"""M5: agreement between the human second rater (review/m5_labels.json) and the automatic labels
(review/out/m5_key.json). Writes review/out/m5_agreement.md.

Part A: per change mode, the rater's tick and the classifier's label are two binary judgements per test;
reported are Cohen's kappa, the classifier's precision and recall against the rater, and the share of tests
on which the whole set of modes matches. Part B: the rater's answer on whether an agent reply names a
mismatch, against the regex flag of scripts/d11_evaluate.py, and the disclosure rate among the
bug-locking suites. Usage: python analysis/m5_agreement.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODES = ['EXPECTED_CHANGED', 'EXCEPTION_EXPECTED', 'FUNCTION_SHADOWED', 'INPUT_CHANGED', 'ASSERT_REMOVED',
         'ASSERT_WEAKENED', 'ASSERT_ADDED', 'SETUP_CHANGED', 'TEST_REWRITTEN']


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    pa, pb = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    labels = json.loads((ROOT / 'review' / 'm5_labels.json').read_text(encoding='utf-8'))
    key = json.loads((ROOT / 'review' / 'out' / 'm5_key.json').read_text(encoding='utf-8'))
    assert labels['seed'] == key['seed']
    a_h, a_k = labels['answers']['a'], key['part_a']
    ids = sorted(a_k)
    lines = ['# M5: second-rater agreement', '', f"Rater export {labels['exported']}; sample seed {key['seed']}.", '',
             f'## Part A: change modes ({len(ids)} repaired tests)', '',
             '| Mode | Rater ticks | Classifier labels | Both | Cohen kappa | Classifier precision | Classifier recall |',
             '|---|---:|---:|---:|---:|---:|---:|']
    for m in MODES:
        pairs = [(m in a_h.get(i, {}).get('modes', []), m in a_k[i]['classifier']) for i in ids]
        h, c, both = sum(p[0] for p in pairs), sum(p[1] for p in pairs), sum(p[0] and p[1] for p in pairs)
        prec = f'{both}/{c}' if c else '-'
        rec = f'{both}/{h}' if h else '-'
        lines.append(f'| {m} | {h} | {c} | {both} | {kappa(pairs):.2f} | {prec} | {rec} |')
    exact = sum(set(a_h.get(i, {}).get('modes', [])) == set(a_k[i]['classifier']) for i in ids)
    lines += ['', f'Identical mode sets: {exact} of {len(ids)}.', '']
    # Split by policy and program version (review item R2, 18 October). The sample was stratified to cover rare
    # modes, so these are agreement figures within strata, not population rates of the modes.
    oracle_c = {'EXPECTED_CHANGED', 'EXCEPTION_EXPECTED', 'FUNCTION_SHADOWED', 'TEST_REWRITTEN', 'INPUT_CHANGED',
                'ASSERT_WEAKENED', 'ASSERT_REMOVED'}
    oracle_h = oracle_c - {'TEST_REWRITTEN'}
    lines += ['### Split by policy and program version', '',
              'The sample is stratified to cover rare modes, so the shares are not population rates. "Any oracle change" is the',
              'trigger of the oracle-lock replay.', '',
              '| Policy, version | Tests | Expected value changed: rater / classifier / both | Any oracle change: rater / classifier / both | Rater\'s expected-value changes the classifier missed, labelled as |',
              '|---|---:|---|---|---|']
    groups = {}
    for i in ids:
        k = a_k[i]
        groups.setdefault((k.get('policy', '?'), k.get('condition', '?')), []).append(i)
    for (policy, cond), members in sorted(groups.items()):
        h_e = sum('EXPECTED_CHANGED' in a_h.get(i, {}).get('modes', []) for i in members)
        c_e = sum('EXPECTED_CHANGED' in a_k[i]['classifier'] for i in members)
        b_e = sum('EXPECTED_CHANGED' in a_h.get(i, {}).get('modes', []) and 'EXPECTED_CHANGED' in a_k[i]['classifier'] for i in members)
        h_o = sum(bool(set(a_h.get(i, {}).get('modes', [])) & oracle_h) for i in members)
        c_o = sum(bool(set(a_k[i]['classifier']) & oracle_c) for i in members)
        b_o = sum(bool(set(a_h.get(i, {}).get('modes', [])) & oracle_h) and bool(set(a_k[i]['classifier']) & oracle_c) for i in members)
        missed = {}
        for i in members:
            if 'EXPECTED_CHANGED' in a_h.get(i, {}).get('modes', []) and 'EXPECTED_CHANGED' not in a_k[i]['classifier']:
                mode_set = '+'.join(sorted(a_k[i]['classifier'])) or 'none'
                missed[mode_set] = missed.get(mode_set, 0) + 1
        lines.append(f"| {policy}, {cond} | {len(members)} | {h_e} / {c_e} / {b_e} | {h_o} / {c_o} / {b_o} | "
                     + (', '.join(f'{k} {v}' for k, v in sorted(missed.items(), key=lambda kv: -kv[1])) or '-') + ' |')
    lines.append('')
    # The modes the paper's argument rests on, as erasure mechanisms: overwrite-style and shadowing.
    b_h, b_k = labels['answers']['b'], key['part_b']
    locked = [i for i in b_k if b_k[i]['kind'] == 'locked']
    control = [i for i in b_k if b_k[i]['kind'] == 'control']
    count = lambda ids_, ans: sum(b_h.get(i, {}).get('answer') == ans for i in ids_)
    lines += [f'## Part B: agent replies ({len(b_k)})', '',
              '| Group | Rater YES | Rater NO | Rater UNCLEAR | Regex flag | Regex flag and rater YES |', '|---|---:|---:|---:|---:|---:|']
    for name, group in (('Suites that lock the bug in', locked), ('Controls (correct programs)', control)):
        lines.append(f"| {name} ({len(group)}) | {count(group, 'YES')} | {count(group, 'NO')} | {count(group, 'UNCLEAR')} | "
                     f"{sum(b_k[i]['regex_flag'] for i in group)} | "
                     f"{sum(b_k[i]['regex_flag'] and b_h.get(i, {}).get('answer') == 'YES' for i in group)} |")
    by_arm = {}
    for i in locked:
        arm = b_k[i]['arm']
        by_arm.setdefault(arm, [0, 0])
        by_arm[arm][0] += 1
        by_arm[arm][1] += b_h.get(i, {}).get('answer') == 'YES'
    lines += ['', 'Bug-locking suites whose final reply names the mismatch (rater YES), per arm:', '']
    lines += [f'- {arm}: {yes} of {n}' for arm, (n, yes) in sorted(by_arm.items())]
    out = ROOT / 'review' / 'out' / 'm5_agreement.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
