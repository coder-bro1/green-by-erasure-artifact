import ast
import builtins
import json
import time

from .execute import execute
from .generate import code_block, oracle_locked, parse_suite, suite_hash


def literal(node):
    try:
        ast.literal_eval(node)
        return True
    except (ValueError, SyntaxError, TypeError):
        return False


def template_repair(source, prelude, outcome):
    tree = ast.parse(prelude + '\n' + source)
    frames = outcome.get('frames', [])
    test_frames = [f for f in frames if f['file'] == 'test_generated.py']
    line = test_frames[-1]['line'] if test_frames else None
    def rendered(action):
        parsed = parse_suite(ast.unparse(ast.fix_missing_locations(tree)))
        return parsed['tests'][0]['source'], parsed['prelude'], action
    # Exact executed assertion/statement only; never infer a value by executing the PUT again.
    target = next((n for n in ast.walk(tree) if isinstance(n, ast.Assert)
                   and n.lineno <= (line or -1) <= n.end_lineno), None)
    if outcome['outcome'] == 'ASSERT_FAIL' and target:
        expr = target.test
        if isinstance(expr, ast.Compare) and len(expr.ops) == 1 and isinstance(expr.ops[0], ast.Eq):
            left, right = expr.left, expr.comparators[0]
            left_lit, right_lit = literal(left), literal(right)
            other = right if left_lit else left
            comparisons = outcome.get('comparisons', [])
            if left_lit != right_lit and any(isinstance(n, ast.Call) for n in ast.walk(other)) and comparisons:
                observed = comparisons[-1]['right' if left_lit else 'left']
                if observed['literal']:
                    replacement = ast.parse(observed['repr'], mode='eval').body
                    if left_lit:
                        expr.left = replacement
                    else:
                        expr.comparators[0] = replacement
                    return rendered('T3')
        flip = isinstance(expr, ast.Call) or (isinstance(expr, ast.UnaryOp)
                    and isinstance(expr.op, ast.Not) and isinstance(expr.operand, ast.Call))
        none_check = (isinstance(expr, ast.Compare) and len(expr.ops) == 1 and
                      isinstance(expr.ops[0], (ast.Is, ast.IsNot)) and
                      isinstance(expr.comparators[0], ast.Constant) and expr.comparators[0].value is None)
        if flip:
            target.test = expr.operand if isinstance(expr, ast.UnaryOp) else ast.UnaryOp(op=ast.Not(), operand=expr)
            return rendered('T2')
        if none_check:
            expr.ops[0] = ast.IsNot() if isinstance(expr.ops[0], ast.Is) else ast.Is()
            return rendered('T2')
    if outcome['outcome'] == 'PUT_EXCEPTION' and line:
        kind = outcome.get('exception_type', '')
        cls = getattr(builtins, kind, None)
        if not isinstance(cls, type) or not issubclass(cls, BaseException):
            return None
        for parent in ast.walk(tree):
            for field, value in ast.iter_fields(parent):
                if isinstance(value, list):
                    for i, node in enumerate(value):
                        if isinstance(node, ast.stmt) and not isinstance(node, (ast.FunctionDef, ast.With,
                                ast.If, ast.For, ast.While, ast.Try)) and node.lineno <= line <= node.end_lineno:
                            wrapper = ast.With(items=[ast.withitem(context_expr=ast.Call(
                                func=ast.Attribute(value=ast.Name(id='pytest', ctx=ast.Load()),
                                attr='raises', ctx=ast.Load()), args=[ast.Name(id=kind, ctx=ast.Load())],
                                keywords=[]))], body=[node])
                            value[i] = wrapper
                            tree.body.insert(0, ast.Import(names=[ast.alias(name='pytest')]))
                            return rendered('T4')
    return None


def judge_parse(text):
    # Models often wrap the JSON in a ```json fence, which code_block does not recognise.
    # Parse the outermost {...} object instead of relying on the fence language.
    try:
        raw = code_block(text)
        start, end = raw.find('{'), raw.rfind('}')
        value = json.loads(raw[start:end + 1] if 0 <= start < end else raw)
        if value['verdict'] in ('BUG', 'TEST_WRONG', 'UNSURE') and isinstance(value['reason'], str):
            return value
    except (ValueError, KeyError, TypeError):
        pass
    return {'verdict': 'UNSURE', 'reason': 'Unparseable judge response'}


JUDGE_PROMPT, JUDGE_ABLATION_PROMPT = 'judge_v2b', 'judge_with_code_v2b'
V2B_VERDICTS = {'YES': 'BUG', 'NO': 'TEST_WRONG', 'UNCLEAR': 'UNSURE'}


def judge_v2b_parse(text):
    """Parser frozen with the v2b prompt (Phase 2 decision Q1); same JSON extraction as the pilot replay.

    YES (the specification guarantees the test passes, so the failure is the program's) -> BUG,
    NO -> TEST_WRONG, UNCLEAR -> UNSURE, anything else or unparseable -> UNSURE.
    """
    raw = text
    for fence in ('```json', '```'):
        if fence in raw:
            raw = raw.split(fence, 1)[1].split('```', 1)[0]
            break
    start, end = raw.find('{'), raw.rfind('}')
    try:
        value = json.loads(raw[start:end + 1]) if 0 <= start < end else None
    except ValueError:
        value = None
    value = value if isinstance(value, dict) else {}
    answer = value.get('answer')
    answer = answer if isinstance(answer, str) and answer in V2B_VERDICTS else ''
    reason = value.get('reason') if isinstance(value.get('reason'), str) else ''
    return {'verdict': V2B_VERDICTS.get(answer, 'UNSURE'), 'answer': answer,
            'reason': reason if answer else 'Unparseable or invalid judge response'}


def repair_policy(policy, suite, initial, context, client, unit_id, judge_ablation=True):
    started = time.monotonic()
    records = []
    for index, generated in enumerate(suite['tests']):
        test_id = f'{unit_id}/t{index}'
        source, prelude = generated['source'], suite['prelude']
        outcome = initial[index]
        versions = [{'round': 0, 'source': source, 'prelude': prelude, 'outcome': outcome,
                     'action': 'GENERATED', 'accepted': True}]
        record = {'test_id': test_id, 'versions': versions, 'judge_verdict': '',
                  'judge_with_code_verdict': '', 'n_llm_calls': 0}
        status = 'DROPPED'
        for round_no in range(4):
            kind = outcome['outcome']
            if kind == 'PASS':
                status = 'KEPT'
                break
            if policy == 'P1':
                break
            fields = dict(program=context['program'], spec=context['spec'],
                          test=prelude + '\n' + source, feedback=outcome.get('output', kind))
            if policy == 'P4' and kind in ('ASSERT_FAIL', 'PUT_EXCEPTION', 'TIMEOUT'):
                # Judge v2b sees the specification and the test only: no implementation, no traceback
                # and no observed behaviour. The D10 ablation adds the implementation and nothing else.
                judge_fields = {'spec': context['spec'], 'test': prelude + '\n' + source}
                decision = judge_v2b_parse(client.call(JUDGE_PROMPT, judge_fields, unit_id=unit_id,
                    purpose='judge', policy=policy, test_id=test_id, round=round_no))
                record.update(judge_verdict=decision['verdict'], judge_answer=decision['answer'],
                              judge_reason=decision['reason'])
                record['n_llm_calls'] += 1
                if judge_ablation:
                    ablation = judge_v2b_parse(client.call(JUDGE_ABLATION_PROMPT,
                        dict(judge_fields, program=context['program']), unit_id=unit_id,
                        purpose='judge_with_code', policy=policy, test_id=test_id, round=round_no))
                    record['judge_with_code_verdict'] = ablation['verdict']
                    record['n_llm_calls'] += 1
                # Quarantine retains original bytes, even after a setup repair. This follows
                # the review protocol's stricter invariant; record which version was judged.
                record['judged_source'] = source
                record['judged_outcome'] = outcome
                if decision['verdict'] != 'TEST_WRONG':
                    status = 'QUARANTINED'
                    source, prelude = generated['source'], suite['prelude']
                    outcome = initial[index]
                break
            if round_no == 3 or (policy == 'P2' and kind == 'TIMEOUT'):
                break
            repaired = template_repair(source, prelude, outcome) if policy == 'P2' else None
            if repaired:
                candidate, candidate_prelude, action = repaired
            else:
                purpose = ('free_repair' if policy == 'P3' else
                           'fix_broken' if kind in ('TEST_ERROR', 'COLLECT_ERROR') else 'overwrite_fallback')
                response = client.call(purpose + '_v1', fields, unit_id=unit_id, purpose=purpose,
                                       policy=policy, test_id=test_id, round=round_no + 1)
                record['n_llm_calls'] += 1
                action = purpose
                try:
                    parsed = parse_suite(response)
                    if len(parsed['tests']) != 1:
                        raise ValueError('Repair must contain exactly one test')
                    candidate = parsed['tests'][0]['source']
                    candidate_prelude = parsed['prelude']
                except (SyntaxError, ValueError):
                    versions.append({'round': round_no + 1, 'source': response, 'prelude': prelude,
                                     'outcome': {'outcome': 'COLLECT_ERROR'}, 'action': action,
                                     'accepted': False, 'rejection': 'PARSE_ERROR'})
                    continue
            accepted = policy != 'P4' or oracle_locked(suite['prelude'] + '\n' + generated['source'],
                                                       candidate_prelude + '\n' + candidate)
            if accepted:
                source, prelude = candidate, candidate_prelude
                outcome = execute(context['program'], prelude, source, support=context.get('support'),
                                  runtime=context.get('runtime'))
            versions.append({'round': round_no + 1, 'source': candidate, 'prelude': candidate_prelude,
                             'outcome': outcome, 'action': action, 'accepted': accepted,
                             'rejection': '' if accepted else 'ORACLE_LOCK'})
        record.update(final_status=status, source=source, prelude=prelude,
                      outcome_put=outcome['outcome'])
        records.append(record)
    return {'policy': policy, 'input_hash': suite_hash(suite), 'tests': records,
            'wall_time_s': time.monotonic() - started}
