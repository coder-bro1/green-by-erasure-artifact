"""C2 step 4: adjudication files for the cases where the two raters differ.

Writes, from review/c2_labels/c2_cases.csv (rater B, the user) and review/c2_labels_claude/c2_labels_claude.csv
(rater A, Claude):
- review/c2_labels/c2_adjudication.csv: one row per differing case with both labels and reasons and empty FINAL
  columns (UTF-8 with BOM for Excel);
- review/c2_labels/C2_ADJUDICATION_READER.html: the reader cards of those cases with both labels on each card.
The instructions are in review/c2_labels/C2_ADJUDICATION_INSTRUCTIONS.md. Runs in .venv-c2.
Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_adjudication.py
"""
import csv
import html
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import c2_reader  # noqa: E402

NAMES = {'I': 'intended change', 'W': 'wrong test repaired', 'E': 'possible erasure', 'M': 'no real change', 'U': "can't tell"}


def main():
    labels_dir = ROOT / 'review' / 'c2_labels'
    u = pd.read_csv(labels_dir / 'c2_cases.csv', encoding='utf-8-sig')
    c = pd.read_csv(ROOT / 'review' / 'c2_labels_claude' / 'c2_labels_claude.csv')
    assert list(u.case) == list(c.case)
    why = [x for x in u.columns if x.startswith('WHY')][0]
    says = [x for x in u.columns if x.startswith('SAYS')][0]
    rows, boxes = [], {}
    for i, r in u.iterrows():
        bw, bs = str(r[why]).strip().upper(), str(r[says]).strip().upper()
        aw, as_ = c.at[i, 'why'], c.at[i, 'says_test_changed']
        if bw == aw and bs == as_:
            continue
        note = r['note (optional)'] if isinstance(r['note (optional)'], str) else ''
        rows.append({'case': r.case, 'link': r.link, 'title': r.title, 'changed_asserts': r.changed_asserts,
                     'YOUR WHY': bw, 'YOUR SAYS': bs, 'your note': note,
                     'CLAUDE WHY': aw, 'CLAUDE SAYS': as_, 'Claude reason': c.at[i, 'reason'],
                     'FINAL WHY (I / W / E / M / U)': '', 'FINAL SAYS (Y / N)': '', 'final note (optional)': ''})
        differ = []
        if bw != aw:
            differ.append('WHY')
        if bs != as_:
            differ.append('SAYS')
        boxes[r.case] = (
            f'<div class="labels"><div><b>You</b>: <b class="l">{bw}</b> ({NAMES[bw]}), SAYS <b>{bs}</b>'
            f'<br><span class="fact">{html.escape(note) or "(no note)"}</span></div>'
            f'<div><b>Claude</b>: <b class="l">{aw}</b> ({NAMES[aw]}), SAYS <b>{as_}</b>'
            f'<br><span class="fact">{html.escape(c.at[i, "reason"])}</span></div></div>'
            f'<p class="fact">Differ on: {" and ".join(differ)}. Your FINAL goes into c2_adjudication.csv.</p>')
    with open(labels_dir / 'c2_adjudication.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    c2_reader.main(out=labels_dir / 'C2_ADJUDICATION_READER.html', only={r['case'] for r in rows}, labels=boxes,
                   heading='C2 adjudication reader',
                   intro=f'The {len(rows)} cases where our labels differ, with both labels on each card. Pick the final '
                         'label for each and write it into <code>c2_adjudication.csv</code>. Rules: '
                         '<code>C2_LABEL_GUIDE.html</code>.')
    print(f'{len(rows)} cases in c2_adjudication.csv')


if __name__ == '__main__':
    main()
