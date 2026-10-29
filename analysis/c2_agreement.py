"""C2 step 4: agreement between the two raters on the 100 sampled agent pull requests.

Inputs: review/c2_labels/c2_cases.csv (second rater, the user) and review/c2_labels_claude/c2_labels_claude.csv
(first rater). Reports Cohen's kappa for WHY (I, W, E, M, U), for the binary question "possible erasure" (E
against the rest), for SAYS TEST CHANGED, the confusion matrix and each rater's counts, and checks the step 2
disclosure regex against both raters. Writes review/out/c2_agreement.md and review/out/c2_disagreements.md (the
cases to settle together). Runs in .venv-c2. Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_agreement.py
"""
import json
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CATS = ['I', 'W', 'E', 'M', 'U']


def current_mask(n_rows):
    """Which sampled cases are still candidates after the authorship filter of 19 October (c2_mine.py): a
    labelled pull request stays in the analysis only if the agent's own commits still change an expected value."""
    import json as _json
    ids = _json.loads((ROOT / 'review' / 'c2_labels' / 'c2_sample.json').read_text(encoding='utf-8'))['pr_ids']
    prs = pd.read_csv(ROOT / 'runs' / 'c2' / 'prs.csv')
    cand = set(prs[prs.expected_changes > 0].pr_id)
    assert len(ids) == n_rows
    return [pid in cand for pid in ids]


def kappa(a, b, cats):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return po, ((po - pe) / (1 - pe) if pe < 1 else 1.0)


def main():
    u = pd.read_csv(ROOT / 'review' / 'c2_labels' / 'c2_cases.csv', encoding='utf-8-sig')
    c = pd.read_csv(ROOT / 'review' / 'c2_labels_claude' / 'c2_labels_claude.csv')
    assert list(u.case) == list(c.case)
    mask = current_mask(len(u))
    u, c = u[mask].reset_index(drop=True), c[mask].reset_index(drop=True)
    why_col = [x for x in u.columns if x.startswith('WHY')][0]
    says_col = [x for x in u.columns if x.startswith('SAYS')][0]
    hu = [str(x).strip().upper() for x in u[why_col]]
    hc = list(c.why)
    su = [str(x).strip().upper() for x in u[says_col]]
    sc = list(c.says_test_changed)
    assert set(hu) <= set(CATS) and set(su) <= {'Y', 'N'}
    lines = ['# C2 step 4: agreement between the two raters', '',
             f'Computed by `analysis/c2_agreement.py`. {len(u)} of the 100 sampled agent pull requests (seed gbe-c2-labels-v2): those',
             'still candidates after the authorship filter of 19 October (only the agent\'s own commits count). Rater A: the',
             'first rater (Claude, labels made from the sheet alone). Rater B: the second rater (the user). Labels before',
             'adjudication.', '']
    po, k = kappa(hu, hc, CATS)
    lines.append(f'- WHY, five labels: observed agreement {100 * po:.0f}%, Cohen kappa {k:.2f}.')
    eu, ec = ['E' if x == 'E' else 'other' for x in hu], ['E' if x == 'E' else 'other' for x in hc]
    po_e, k_e = kappa(eu, ec, ['E', 'other'])
    lines.append(f'- Possible erasure (E against the rest): observed agreement {100 * po_e:.0f}%, kappa {k_e:.2f}.')
    clear = [(a, b) for a, b in zip(hc, hu) if a != 'U' and b != 'U']
    po_c, k_c = kappa([a for a, _ in clear], [b for _, b in clear], ['I', 'W', 'E', 'M'])
    lines.append(f'- WHY on the {len(clear)} cases neither rater marked U: agreement {100 * po_c:.0f}%, kappa {k_c:.2f}.')
    po_s, k_s = kappa(su, sc, ['Y', 'N'])
    lines.append(f'- SAYS TEST CHANGED: observed agreement {100 * po_s:.0f}%, kappa {k_s:.2f}.')
    lines += ['', '| Label | Rater A (Claude) | Rater B (user) |', '|---|---:|---:|']
    for cat in CATS:
        lines.append(f'| {cat} | {hc.count(cat)} | {hu.count(cat)} |')
    lines.append(f"| SAYS = Y | {sc.count('Y')} | {su.count('Y')} |")
    lines += ['', 'Confusion matrix (rows rater A, columns rater B):', '', '| A \\ B | ' + ' | '.join(CATS) + ' |',
              '|---|' + '---:|' * len(CATS)]
    cm = Counter(zip(hc, hu))
    for a in CATS:
        lines.append(f'| {a} | ' + ' | '.join(str(cm[(a, b)]) for b in CATS) + ' |')
    # Step 2 regex against the raters.
    step2 = pd.read_csv(ROOT / 'runs' / 'c2' / 'step2.csv').set_index('url')
    flag = [bool(step2.at[link, 'explains_test_change']) if link in step2.index else None for link in u.link]
    for name, labs in (('A', sc), ('B', su)):
        tp = sum(f and l == 'Y' for f, l in zip(flag, labs))
        fp = sum(f and l == 'N' for f, l in zip(flag, labs))
        fn = sum((not f) and l == 'Y' for f, l in zip(flag, labs))
        lines.append(f'- Step 2 disclosure regex against rater {name}: {tp + fp} flagged, {tp} of them labelled Y '
                     f'(precision {100 * tp / max(1, tp + fp):.0f}%); {tp + fn} labelled Y, {tp} flagged (recall {100 * tp / max(1, tp + fn):.0f}%).')
    lines.append('')
    (ROOT / 'review' / 'out' / 'c2_agreement.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))
    dis = ['# C2 step 4: cases where the raters differ', '',
           'To settle together. Rater A is Claude, rater B the user. The reader page has the full case.', '']
    n = 0
    for i, row in u.iterrows():
        a_w, b_w, a_s, b_s = hc[i], hu[i], sc[i], su[i]
        if a_w == b_w and a_s == b_s:
            continue
        n += 1
        note = row.get('note (optional)')
        dis += [f"## {row.case}: WHY A={a_w} B={b_w}; SAYS A={a_s} B={b_s}", '',
                f"{row.title}", '', f"- A's reason: {c.at[i, 'reason']}",
                f"- B's note: {note if isinstance(note, str) else '(none)'}", f'- {row.link}', '']
    dis.insert(3, f'{n} cases.')
    (ROOT / 'review' / 'out' / 'c2_disagreements.md').write_text('\n'.join(dis) + '\n', encoding='utf-8')
    print(f'{n} cases with a difference written to review/out/c2_disagreements.md')


if __name__ == '__main__':
    main()
