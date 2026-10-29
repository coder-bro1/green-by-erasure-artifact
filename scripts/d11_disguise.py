"""Disguised HumanEvalFix programs for the D11 contamination control (decided by the user on 11 October 2026).

For each of the 40 programs in configs/phase2_seed_subset.json, the buggy and the fixed version are
transformed identically:
  - every function, parameter and local name in SPEC is renamed (AST), string contents untouched;
  - module-level string constants (HumanEval/64's FIX) are dropped;
  - the entry function's docstring is replaced by a description written for this study, followed by
    examples whose inputs are new and whose outputs are computed by running the disguised FIXED program;
  - helper functions get a one-line docstring or none.
So the bug is unchanged, the examples are correct by construction, and no original example appears.

`build` writes runs/d11/disguised_tasks.json; `verify` checks, for every program:
  1. the disguised fixed version passes HumanEval's own hidden tests and the buggy version fails them
     (tests run against the disguised module through aliases to the original names);
  2. no original function name remains in either version;
  3. the buggy/fixed line diff has the same size as for the original programs;
  4. whether the docstring examples expose the bug (buggy output differs) matches the original docstring.
Usage: python scripts/d11_disguise.py build | verify
"""
import ast
import os
import json
import re
import subprocess
import sys
import tempfile
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.benchmarks import download, program  # noqa: E402

OUT = ROOT / 'runs' / 'd11' / 'disguised_tasks.json'


def private_tmp():
    """A temporary folder inside a parent folder private to this process. pytest inspects the paths next to
    its working folder during collection; sibling folders created and deleted by other processes make it
    fail with FileNotFoundError, so concurrent runs must not share a parent folder."""
    parent = ROOT / '.scratch' / 'd11eval' / str(os.getpid())
    parent.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=parent)

# pid: (renames, description of the entry function, example argument lists, helper docstrings)
SPEC = {
 'Python/5': ({'intersperse': 'weave_separator', 'numbers': 'values', 'delimeter': 'sep', 'result': 'out', 'n': 'item'},
     'Return a new list in which sep is placed between every pair of neighbouring items of values.',
     ['[7, 8], 0', '[5, 5, 5], -1', '[], 2'], {}),
 'Python/8': ({'sum_product': 'total_and_multiple', 'numbers': 'values', 'sum_value': 'acc_sum', 'prod_value': 'acc_prod', 'n': 'v'},
     'Return a pair (s, p): s is the sum of all integers in values and p is their product. For an empty list, s is 0 and p is 1.',
     ['[2, 5]', '[-3, 4, 1]'], {}),
 'Python/9': ({'rolling_max': 'running_peaks', 'numbers': 'values', 'running_max': 'peak', 'result': 'out', 'n': 'v'},
     'Return a list whose element i is the largest value among values[0], ..., values[i].',
     ['[2, 1, 5, 3, 6]'], {}),
 'Python/10': ({'make_palindrome': 'shortest_mirror_extension', 'is_palindrome': 'reads_same', 'string': 'text', 'beginning_of_suffix': 'cut'},
     'Return the shortest palindrome that starts with text, formed by appending characters to the end of text.',
     ["''", "'abc'", "'abcb'"], {'reads_same': 'Return True if text is the same read backwards.'}),
 'Python/12': ({'longest': 'first_longest', 'strings': 'words', 'maxlen': 'top', 's': 'w', 'x': 'item'},
     'Return the longest string in words. When several strings share the maximum length, return the earliest one. Return None for an empty list.',
     ["['xy', 'abc', 'q']", "['no', 'at']", '[]'], {}),
 'Python/13': ({'greatest_common_divisor': 'common_factor_max', 'a': 'p', 'b': 'q'},
     'Return the greatest common divisor of the integers p and q.',
     ['12, 18', '7, 13'], {}),
 'Python/19': ({'sort_numbers': 'order_number_words', 'numbers': 'phrase', 'value_map': 'rank', 'x': 'w'},
     "phrase holds number words from 'zero' to 'nine' separated by spaces. Return the same words, separated by single spaces, ordered from the smallest number to the largest.",
     ["'nine two six'"], {}),
 'Python/24': ({'largest_divisor': 'biggest_proper_factor', 'n': 'num', 'i': 'd'},
     'Return the largest integer smaller than num that divides num exactly.',
     ['21', '32'], {}),
 'Python/27': ({'flip_case': 'invert_letter_case', 'string': 'text'},
     'Return text with every lowercase letter changed to uppercase and every uppercase letter changed to lowercase.',
     ["'PyThon 3'"], {}),
 'Python/31': ({'is_prime': 'has_no_divisors', 'n': 'num', 'k': 'd'},
     'Return True when num is a prime number and False otherwise. Numbers below 2 are not prime.',
     ['9', '29', '1', '97'], {}),
 'Python/38': ({'decode_cyclic': 'unscramble_triples', 'encode_cyclic': 'scramble_triples', 's': 'text', 'groups': 'chunks', 'group': 'chunk', 'i': 'k'},
     'Undo scramble_triples: given a string produced by scramble_triples, return the string it was produced from.',
     [],  # the original docstring has no examples
     {'scramble_triples': 'Split text into consecutive groups of three characters and move the first character of every full group to its end; a shorter final group is left unchanged.'}),
 'Python/43': ({'pairs_sum_to_zero': 'has_opposite_pair', 'l': 'nums', 'l1': 'a'},
     'Return True when two different positions of nums hold values that add up to zero, and False otherwise.',
     ['[4, -4, 2]', '[0, 3]', '[5]'], {}),
 'Python/56': ({'correct_bracketing': 'angles_balanced', 'brackets': 'marks', 'depth': 'level', 'b': 'ch'},
     "marks contains only '<' and '>'. Return True when every '<' is closed by a later '>' and no '>' appears before a matching '<'; otherwise return False.",
     ["'<<>>'", "'><'", "'<'"], {}),
 'Python/57': ({'monotonic': 'is_one_direction', 'l': 'seq'},
     'Return True when the elements of seq never decrease or never increase, and False otherwise.',
     ['[1, 1, 3]', '[5, 2, 2, 0]', '[2, 9, 4]'], {}),
 'Python/62': ({'derivative': 'poly_slope_coeffs', 'xs': 'coeffs', 'i': 'k', 'x': 'c'},
     'coeffs lists the coefficients of a polynomial from the constant term upward: coeffs[0] + coeffs[1] * t + coeffs[2] * t**2 + .... Return the coefficients of its derivative in the same order.',
     ['[5, 0, 3]', '[2, 4]'], {}),
 'Python/63': ({'fibfib': 'tri_sum_seq', 'n': 'k'},
     'A sequence is defined by s(0) = 0, s(1) = 0, s(2) = 1 and s(k) = s(k - 1) + s(k - 2) + s(k - 3) for k > 2. Return s(k).',
     ['2', '6', '9'], {}),
 'Python/64': ({'vowels_count': 'count_vowel_sounds', 's': 'word', 'vowels': 'letters', 'n_vowels': 'total', 'c': 'ch'},
     "Return how many vowels word contains. The vowels are a, e, i, o and u in either case; the letter y (or Y) also counts, but only when it is the last character of word.",
     ["'sky'", "'Queue'", "'Banana'"], {}),
 'Python/65': ({'circular_shift': 'rotate_digits', 'x': 'num', 'shift': 'steps', 's': 'digits'},
     'Rotate the decimal digits of num to the right by steps positions and return the result as a string. If steps is larger than the number of digits, return the digits in reverse order.',
     ['4567, 1', '89, 3'], {}),
 'Python/67': ({'fruit_distribution': 'remaining_mangoes', 's': 'note', 'n': 'total', 'lis': 'counts', 'i': 'tok'},
     "note has the form '<a> apples and <b> oranges'. A basket holds total fruits, each an apple, an orange or a mango. Return the number of mangoes.",
     ["'4 apples and 9 oranges', 30", "'0 apples and 0 oranges', 7"], {}),
 'Python/72': ({'will_it_fly': 'can_lift', 'q': 'load', 'w': 'limit'},
     'Return True when the list load reads the same forwards and backwards and its sum is at most limit; otherwise return False.',
     ['[4, 1, 4], 10', '[4, 1, 4], 8', '[2, 5], 9', '[6], 7'], {}),
 'Python/74': ({'total_match': 'fewer_letters', 'lst1': 'first', 'lst2': 'second', 'l1': 'n1', 'l2': 'n2', 'st': 'w'},
     'Count the characters in all strings of first and in all strings of second. Return the list with the smaller total; when both totals are equal, return first.',
     ["['ab', 'c'], ['xyz', 'w']", "['long'], ['a', 'b']", '[], []'], {}),
 'Python/80': ({'is_happy': 'no_close_repeats', 's': 'text'},
     'Return True when text has at least three characters and every window of three neighbouring characters holds three different characters; otherwise return False.',
     ["'xyzx'", "'xyx'", "'pq'"], {}),
 'Python/82': ({'prime_length': 'length_is_prime', 'string': 'text', 'l': 'size', 'i': 'd'},
     'Return True when the number of characters in text is a prime number, and False otherwise.',
     ["'abc'", "'pythons'", "'banana'"], {}),
 'Python/85': ({'add': 'even_values_at_odd_slots', 'lst': 'values', 'i': 'k'},
     'values is a non-empty list of integers. Return the sum of the even numbers found at odd indexes (1, 3, 5, ...).',
     ['[1, 6, 3, 8, 2]'], {}),
 'Python/97': ({'multiply': 'last_digit_product', 'a': 'x', 'b': 'y'},
     'Return the product of the last decimal digits of the integers x and y.',
     ['37, 54', '-21, 46', '1990, 13'], {}),
 'Python/107': ({'even_odd_palindrome': 'palindrome_parity_counts', 'is_palindrome': 'mirror', 'n': 'limit',
                 'even_palindrome_count': 'evens', 'odd_palindrome_count': 'odds', 'i': 'k'},
     'Consider the integers from 1 to limit inclusive (1 <= limit <= 1000). Return a pair (even_count, odd_count) with the number of even and of odd palindromic numbers among them.',
     ['5', '22'], {}),
 'Python/108': ({'count_nums': 'positive_digit_sums', 'arr': 'values', 'digits_sum': 'signed_digit_total', 'neg': 'sign', 'n': 'm', 'x': 'v'},
     'Return how many integers in values have a digit sum greater than zero, where the first digit of a negative number counts as negative (for example -45 gives -4 + 5 = 1).',
     ['[-12, 3, 0]', '[24, -8]', '[]'], {}),
 'Python/111': ({'histogram': 'most_frequent_letters', 'test': 'text', 'dict1': 'counts', 'list1': 'parts', 't': 'best', 'i': 'item'},
     'text holds lowercase letters separated by spaces. Return a dictionary that maps each letter occurring most often to its number of occurrences; all letters tied for the maximum are included. An empty string gives an empty dictionary.',
     ["'p q p'", "'z y'", "''"], {}),
 'Python/112': ({'reverse_delete': 'strip_and_mirror_check', 's': 'text', 'c': 'banned', 'char': 'ch'},
     'Remove from text every character that also occurs in banned. Return a pair: the remaining string, and True if it reads the same backwards or False if it does not.',
     ["'racecar', 'x'", "'banana', 'b'", "'level', 'v'"], {}),
 'Python/117': ({'select_words': 'words_with_consonants', 's': 'sentence', 'n': 'count', 'result': 'found', 'word': 'w',
                 'n_consonants': 'total', 'i': 'k'},
     'Return, in their original order, the words of sentence (split on whitespace) that contain exactly count consonants. sentence contains only letters and spaces; an empty sentence gives an empty list.',
     ["'Big brown fox', 2", "'', 1"], {}),
 'Python/125': ({'split_words': 'break_text', 'txt': 'text', 'i': 'ch'},
     'If text contains a space, return text split on whitespace. Otherwise, if it contains a comma, return it split on commas. Otherwise return the number of lowercase letters at an odd position in the alphabet when a is position 0 (b, d, f, ...).',
     ["'one two'", "'red,green'", "'bdx'"], {}),
 'Python/126': ({'is_sorted': 'ascending_with_few_repeats', 'lst': 'nums', 'count_digit': 'seen', 'i': 'k'},
     'nums holds non-negative integers. Return True when the list is in non-decreasing order and no value appears more than twice; otherwise return False.',
     ['[0, 4, 4, 9]', '[3, 3, 3]', '[2, 1]', '[7]'], {}),
 'Python/130': ({'tri': 'odd_even_series', 'n': 'count', 'my_tri': 'seq', 'i': 'k'},
     'A series t is defined by t(0) = 1, t(1) = 3, t(k) = 1 + k / 2 for even k, and t(k) = t(k - 1) + t(k - 2) + t(k + 1) for odd k >= 3, where t(k + 1) follows the even rule. Return the list [t(0), t(1), ..., t(count)].',
     ['0', '5'], {}),
 'Python/141': ({'file_name_check': 'validate_filename', 'file_name': 'name', 'suf': 'allowed', 'lst': 'parts', 't': 'digits', 'x': 'ch'},
     "Return 'Yes' if name is a valid file name and 'No' otherwise. A valid name contains exactly one dot; the part before the dot is non-empty and starts with a Latin letter (a-z or A-Z); the part after the dot is 'txt', 'exe' or 'dll'; and the whole name contains at most three digits.",
     ["'report7.exe'", "'7report.exe'", "'x1234.txt'"], {}),
 'Python/143': ({'words_in_sentence': 'keep_prime_length_words', 'sentence': 'phrase', 'new_lst': 'kept', 'word': 'w', 'flg': 'composite', 'i': 'd'},
     'phrase contains words of letters separated by single spaces. Return a string of the words whose length is a prime number, in their original order, separated by single spaces.',
     ["'we built a large house'"], {}),
 'Python/146': ({'specialFilter': 'count_odd_edged', 'nums': 'values', 'count': 'total', 'num': 'v', 'odd_digits': 'odd', 'number_as_string': 'text'},
     'Return how many numbers in values are greater than 10 and have both an odd first digit and an odd last digit.',
     ['[31, 25, 12, 9]', '[57, -73]'], {}),
 'Python/148': ({'bf': 'planets_between', 'planet1': 'inner', 'planet2': 'outer', 'planet_names': 'order',
                 'planet1_index': 'a_idx', 'planet2_index': 'b_idx'},
     'The planets in order of distance from the Sun are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune. Return a tuple of the planets strictly between inner and outer, nearest to the Sun first. Return an empty tuple if either name is not one of these planets or both names are the same.',
     ["'Venus', 'Jupiter'", "'Saturn', 'Earth'"], {}),
 'Python/149': ({'sorted_list_sum': 'even_length_words_sorted', 'lst': 'words', 'new_lst': 'kept', 'i': 'w'},
     'Remove the strings of odd length from words and return the remaining strings sorted by length; strings of equal length are in alphabetical order.',
     ["['dd', 'c', 'ab', 'eeee']"], {}),
 'Python/151': ({'double_the_difference': 'sum_odd_squares', 'lst': 'nums', 'i': 'x'},
     'Return the sum of the squares of the odd positive integers in nums. Negative numbers and numbers that are not integers are ignored; an empty list gives 0.',
     ['[3, 4, 1.5]', '[-5, 7]', '[]'], {}),
 'Python/154': ({'cycpattern_check': 'contains_rotation', 'a': 'text', 'b': 'word', 'l': 'size', 'pat': 'doubled'},
     'Return True when word, or any rotation of word, occurs as a substring of text; otherwise return False.',
     ["'network', 'orkw'", "'abcde', 'eab'", "'abc', 'cb'"], {}),
}


# Informal original examples ('Input: 3 / Output: (1, 2)', unquoted strings), transcribed into calls so that
# whether the original examples expose the bug is computed, not assumed.
ORIGINAL_CALLS = {
 'Python/80': ["is_happy('a')", "is_happy('aa')", "is_happy('abcd')", "is_happy('aabb')", "is_happy('adb')", "is_happy('xyy')"],
 'Python/107': ['even_odd_palindrome(3)', 'even_odd_palindrome(12)'],
 'Python/112': ["reverse_delete('abcde', 'ae')", "reverse_delete('abcdef', 'b')", "reverse_delete('abcdedcba', 'ab')"],
 'Python/143': ["words_in_sentence('This is a test')", "words_in_sentence('lets go for swimming')"],
}


class Renamer(ast.NodeTransformer):
    def __init__(self, names):
        self.names = names

    def visit_Name(self, node):
        node.id = self.names.get(node.id, node.id)
        return node

    def visit_arg(self, node):
        node.arg = self.names.get(node.arg, node.arg)
        return node

    def visit_FunctionDef(self, node):
        node.name = self.names.get(node.name, node.name)
        self.generic_visit(node)
        return node


def set_docstring(function, text):
    body = function.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    function.body = ([ast.Expr(ast.Constant(text))] if text else []) + (body or [ast.Pass()])


def run_call(source, call, timeout=10):
    """Evaluate one call against a program in a fresh interpreter; return repr of the result or an error tag."""
    with private_tmp() as d:
        Path(d, 'solution.py').write_text(source, encoding='utf-8')
        code = f'import solution\nprint(repr(solution.{call}))'
        try:
            p = subprocess.run([sys.executable, '-I', '-c', 'import sys; sys.path.insert(0, ".")\n' + code],
                               cwd=d, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return '<timeout>'
        return p.stdout.strip() if p.returncode == 0 else '<error: ' + (p.stderr.strip().splitlines() or ['?'])[-1] + '>'


def disguise(row, condition, spec, docstring):
    names, _, _, helper_docs = spec
    tree = ast.parse(program(row, condition))
    tree.body = [n for n in tree.body if not (isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant)
                                             and isinstance(n.value.value, str))]
    Renamer(names).visit(tree)
    entry = names[row['entry_point']]
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name == entry:
                set_docstring(node, docstring)
            elif node.name in helper_docs:
                set_docstring(node, helper_docs[node.name])
            else:
                set_docstring(node, None)
    return ast.unparse(ast.fix_missing_locations(tree)) + '\n'


def build():
    rows = {r['task_id']: r for r in download()[0]}
    tasks = {}
    for pid in json.load(open(ROOT / 'configs' / 'phase2_seed_subset.json'))['pairs']:
        spec = SPEC[pid]
        names, description, examples, _ = spec
        entry = names[rows[pid]['entry_point']]
        draft = disguise(rows[pid], 'fixed', spec, description)
        lines = []
        for args in examples:
            lines += [f'>>> {entry}({args})', run_call(draft, f'{entry}({args})')]
        doc = description + ('\n\n' + '\n'.join(lines) if lines else '')
        doc = '\n'.join(('    ' + l) if i and l else l for i, l in enumerate(doc.splitlines())) + '\n    '
        tasks[pid] = {'pair_id': pid, 'entry_point': entry, 'original_entry_point': rows[pid]['entry_point'],
                      'names': names, 'programs': {c: disguise(rows[pid], c, spec, doc) for c in ('fixed', 'buggy')}}
        bad = [l for l in lines[1::2] if l.startswith('<')]
        if bad:
            raise SystemExit(f'{pid}: example failed on the fixed program: {bad}')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(tasks, indent=1), encoding='utf-8')
    print(f'{len(tasks)} disguised tasks written to {OUT}')


def hidden_tests(row, task, source, timeout=30):
    # Aliases only for module-level functions; nested helpers cannot be imported.
    top = {n.name for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}
    aliases = '\n'.join(f'from solution import {new} as {old}' for old, new in task['names'].items() if new in top)
    test = aliases + '\n' + row.get('test_setup', '') + '\n' + row['test'] + \
        f"\n\ndef test_benchmark():\n    check({task['original_entry_point']})\n"
    with private_tmp() as d:
        Path(d, 'solution.py').write_text(source, encoding='utf-8')
        Path(d, 'test_benchmark.py').write_text(test, encoding='utf-8')
        try:
            p = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'test_benchmark.py'],
                               cwd=d, capture_output=True, timeout=timeout)
            return 'PASS' if p.returncode == 0 else 'FAIL'
        except subprocess.TimeoutExpired:
            return 'TIMEOUT'


def examples_expose_bug(source_fixed, source_buggy, calls):
    return any(run_call(source_fixed, c) != run_call(source_buggy, c, timeout=5) for c in calls)


def original_calls(row):
    """Calls in the original docstring examples (doctest lines or 'name(args)' examples)."""
    if row['task_id'] in ORIGINAL_CALLS:
        return ORIGINAL_CALLS[row['task_id']]
    doc = ast.get_docstring(next(n for n in ast.walk(ast.parse(row['prompt'])) if isinstance(n, ast.FunctionDef)
                                 and n.name == row['entry_point'])) or ''
    return sorted(set(m.group(0) for m in re.finditer(rf"\b{row['entry_point']}\((?:[^()]|\([^()]*\))*\)", doc)))


def verify():
    rows = {r['task_id']: r for r in download()[0]}
    tasks = json.loads(OUT.read_text(encoding='utf-8'))
    report, problems = [], []
    for pid, task in tasks.items():
        row = rows[pid]
        fixed, buggy = task['programs']['fixed'], task['programs']['buggy']
        hidden = {c: hidden_tests(row, task, task['programs'][c]) for c in ('fixed', 'buggy')}
        # Original function names must not survive as code identifiers or as calls in the docstring;
        # the descriptions may still use ordinary words such as 'longest' or 'derivative'.
        def identifiers(src):
            tree = ast.parse(src)
            return ({n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
                    | {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
                    | {n.arg for n in ast.walk(tree) if isinstance(n, ast.arg)})
        olds = {n.name for n in ast.walk(ast.parse(program(row, 'fixed'))) if isinstance(n, ast.FunctionDef)}
        leftover = sorted((olds & (identifiers(fixed) | identifiers(buggy)))
                          | {o for o in olds if re.search(rf'\b{re.escape(o)}\(', fixed + buggy)})
        diff_size = lambda a, b: len([l for l in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm='', n=0)
                                      if l[:1] in '+-' and l[:3] not in ('+++', '---')])
        orig = diff_size(ast.unparse(ast.parse(program(row, 'buggy'))), ast.unparse(ast.parse(program(row, 'fixed'))))
        new = diff_size(buggy, fixed)
        calls_new = [f"{task['entry_point']}({a})" for a in SPEC[pid][2]]
        exposes_new = examples_expose_bug(fixed, buggy, calls_new)
        exposes_old = examples_expose_bug(program(row, 'fixed'), program(row, 'buggy'), original_calls(row))
        entry = {'pair_id': pid, 'hidden_fixed': hidden['fixed'], 'hidden_buggy': hidden['buggy'],
                 'leftover_names': leftover, 'diff_lines_original': orig, 'diff_lines_disguised': new,
                 'examples_expose_bug_original': exposes_old, 'examples_expose_bug_disguised': exposes_new}
        report.append(entry)
        ok = (hidden['fixed'] == 'PASS' and hidden['buggy'] != 'PASS' and not leftover and orig == new
              and exposes_old == exposes_new)
        if not ok:
            problems.append(entry)
        print(pid, 'ok' if ok else 'PROBLEM', {k: v for k, v in entry.items() if k != 'pair_id'}, flush=True)
    (OUT.parent / 'disguised_verification.json').write_text(json.dumps(report, indent=1), encoding='utf-8')
    print(f'{len(report) - len(problems)} of {len(report)} disguised tasks pass all checks')


if __name__ == '__main__':
    {'build': build, 'verify': verify}[sys.argv[1]]()
