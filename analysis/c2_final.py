"""C2 step 4: final labels after adjudication and the numbers for the paper.

Final label per case: the shared label where both raters agreed, otherwise the adjudicated FINAL from
review/c2_labels/c2_adjudication.csv. Shares are reported for the sample (with Wilson 95% intervals) and,
because the sample is stratified by agent, also weighted back to the 347 pull requests (stratum size / quota).
Writes review/c2_labels/c2_final_labels.csv and review/out/c2_final.md. Runs in .venv-c2.
Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_final.py
"""
import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CATS = ['I', 'W', 'E', 'M', 'U']
NAMES = {'I': 'intended behaviour change', 'W': 'wrong test repaired', 'E': 'possible erasure',
         'M': 'no real change (matcher error)', 'U': "can't tell"}


def current_mask(n_rows):
    """Which sampled cases are still candidates after the authorship filter of 19 October (c2_mine.py): a
    labelled pull request stays in the analysis only if the agent's own commits still change an expected value."""
    import json as _json
    ids = _json.loads((ROOT / 'review' / 'c2_labels' / 'c2_sample.json').read_text(encoding='utf-8'))['pr_ids']
    prs = pd.read_csv(ROOT / 'runs' / 'c2' / 'prs.csv')
    cand = set(prs[prs.expected_changes > 0].pr_id)
    assert len(ids) == n_rows
    return [pid in cand for pid in ids]


def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return f'{100 * p:.0f}% [{100 * max(0, c - h):.0f}, {100 * min(1, c + h):.0f}]'


def main():
    lab = ROOT / 'review' / 'c2_labels'
    u = pd.read_csv(lab / 'c2_cases.csv', encoding='utf-8-sig')
    c = pd.read_csv(ROOT / 'review' / 'c2_labels_claude' / 'c2_labels_claude.csv')
    adj = pd.read_csv(lab / 'c2_adjudication.csv', encoding='utf-8-sig').set_index('case')
    mask = current_mask(len(u))
    u, c = u[mask].reset_index(drop=True), c[mask].reset_index(drop=True)
    why_b = [x for x in u.columns if x.startswith('WHY')][0]
    says_b = [x for x in u.columns if x.startswith('SAYS')][0]
    fw = [x for x in adj.columns if x.startswith('FINAL WHY')][0]
    fs = [x for x in adj.columns if x.startswith('FINAL SAYS')][0]
    quota = json.loads((lab / 'c2_sample.json').read_text(encoding='utf-8'))['quota']
    prs = pd.read_csv(ROOT / 'runs' / 'c2' / 'prs.csv')
    pool = prs[prs.expected_changes > 0].agent.value_counts().to_dict()
    rows = []
    for i, r in u.iterrows():
        b_w, b_s = str(r[why_b]).strip().upper(), str(r[says_b]).strip().upper()
        a_w, a_s = c.at[i, 'why'], c.at[i, 'says_test_changed']
        if r.case in adj.index:
            f_w, f_s = str(adj.at[r.case, fw]).strip().upper(), str(adj.at[r.case, fs]).strip().upper()
            how = 'adjudicated'
        else:
            assert a_w == b_w and a_s == b_s, r.case
            f_w, f_s, how = a_w, a_s, 'agreed'
        assert f_w in CATS and f_s in ('Y', 'N'), r.case
        rows.append({'case': r.case, 'agent': r.agent, 'merged': r.merged, 'link': r.link, 'title': r.title,
                     'rater_A_why': a_w, 'rater_B_why': b_w, 'final_why': f_w,
                     'rater_A_says': a_s, 'rater_B_says': b_s, 'final_says': f_s, 'how': how})
    df = pd.DataFrame(rows)
    df.to_csv(lab / 'c2_final_labels.csv', index=False)
    n = len(df)
    kept = df.agent.value_counts().to_dict()
    weight = {a: pool.get(a, 0) / kept[a] for a in kept}
    wsum = sum(weight[a] for a in df.agent)
    lines = ['# C2 step 4: final labels', '',
             f'Computed by `analysis/c2_final.py`. {len(df)} of the 100 sampled agent pull requests whose own commits change an existing expected value together',
             f"with code (stratified sample of the {sum(pool.values())} candidates after the authorship filter of 19 October, AIDev-pop, Python). Final label: agreed by both raters in "
             f"{(df.how == 'agreed').sum()} cases, adjudicated in {(df.how == 'adjudicated').sum()}. Brackets: Wilson 95% intervals",
             'on the sample; the last column weights the agent strata back to all candidates.', '',
             '| Final WHY | Cases | Share of the sample | Weighted to all candidates |', '|---|---:|---|---:|']
    for cat in CATS:
        k = int((df.final_why == cat).sum())
        wshare = sum(weight[a] for a, w in zip(df.agent, df.final_why) if w == cat) / wsum
        lines.append(f'| {cat}: {NAMES[cat]} | {k} | {wilson(k, n)} | {100 * wshare:.0f}% |')
    real = df[df.final_why != 'M']
    # The 347 are matcher candidates (review item R5): estimate how many change an expectation for real.
    k_real = len(real)
    w_real = sum(weight[a] for a, w in zip(df.agent, df.final_why) if w != 'M') / wsum
    total = sum(pool.values())
    lines += ['', f'- The {total} pull requests are matcher candidates. Real expectation changes (not M): {k_real} of {n} in the '
              f'sample ({wilson(k_real, n)}); weighted to all candidates {100 * w_real:.0f}%, about {round(w_real * total)} pull requests.']
    ks = int((df.final_says == 'Y').sum())
    lines += ['', f"- The description says that an existing expectation changed: {ks} of {n} ({wilson(ks, n)}); "
              f"among the {len(real)} real changes (not M): {int((real.final_says == 'Y').sum())}.",
              f"- Possible erasures (E): {int((df.final_why == 'E').sum())}; of them merged "
              f"{int(((df.final_why == 'E') & (df.merged == 'yes')).sum())}, described as a test change "
              f"{int(((df.final_why == 'E') & (df.final_says == 'Y')).sum())}.",
              f"- Among the real changes the raters could decide (I, W, E): "
              + ', '.join(f"{cat} {int((real.final_why == cat).sum())}" for cat in ('I', 'W', 'E'))
              + f" of {int(real.final_why.isin(['I', 'W', 'E']).sum())}.", '',
              '| Agent | Cases | I | W | E | M | U | Says so (Y) |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for agent in quota:
        s = df[df.agent == agent]
        lines.append(f'| {agent} | {len(s)} | ' + ' | '.join(str(int((s.final_why == cat).sum())) for cat in CATS)
                     + f" | {int((s.final_says == 'Y').sum())} |")
    adjd = df[df.how == 'adjudicated']
    lines += ['', 'Adjudication of the differing cases: final WHY equal to rater A '
              f"{int((adjd.final_why == adjd.rater_A_why).sum())}, to rater B {int((adjd.final_why == adjd.rater_B_why).sum())}, "
              f"to neither {int(((adjd.final_why != adjd.rater_A_why) & (adjd.final_why != adjd.rater_B_why)).sum())} "
              f"(of {len(adjd)}; equal to both where only SAYS differed).", '',
              'Cases with final label E:', '']
    lines += [f"- {r.case} ({r.agent}, {'merged' if r.merged == 'yes' else 'not merged'}): {r.title} ({r.link})"
              for r in df[df.final_why == 'E'].itertuples()]
    (ROOT / 'review' / 'out' / 'c2_final.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
