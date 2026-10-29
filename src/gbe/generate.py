import ast
import re

from .util import digest


def strip_reasoning(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.S).strip()


def code_block(text):
    text = strip_reasoning(text)
    blocks = re.findall(r'```(?:python|py)?\s*\n(.*?)```', text, re.S)
    return blocks[0].strip() if blocks else text.strip()


def parse_suite(text):
    source = code_block(text)
    tree = ast.parse(source)
    tests, prelude = [], ['from solution import *']
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith('test_'):
            tests.append({'name': node.name, 'source': ast.unparse(node)})
        elif isinstance(node, ast.ImportFrom) and node.module == 'solution':
            continue
        elif isinstance(node, ast.Import):
            remaining = [alias for alias in node.names if alias.name != 'solution']
            if remaining:
                node.names = remaining
                prelude.append(ast.unparse(node))
        else:
            prelude.append(ast.unparse(node))
    if not tests or len({test['name'] for test in tests}) != len(tests):
        raise ValueError('Expected unique top-level test functions')
    return {'prelude': '\n'.join(prelude) + '\n', 'tests': tests, 'parse_status': 'OK'}


def suite_hash(suite):
    return digest({'prelude': suite['prelude'], 'tests': suite['tests']})


def oracle_literals(source):
    tree = ast.parse(source)
    literals = []
    for assertion in ast.walk(tree):
        if not isinstance(assertion, ast.Assert):
            continue
        for node in ast.walk(assertion):
            try:
                ast.literal_eval(node)
            except (ValueError, SyntaxError, TypeError):
                continue
            literals.append(ast.dump(node, include_attributes=False))
    return literals


def oracle_locked(before, after):
    try:
        return oracle_literals(before) == oracle_literals(after)
    except SyntaxError:
        return False
