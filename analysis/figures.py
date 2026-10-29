"""Figures for the Phase 2 report and the paper, as pgfplots code (no plotting library in the study environment).

Writes figures/<name>.tikz (a tikzpicture the paper can \\input) and figures/<name>.tex (a standalone wrapper),
then compiles each wrapper to figures/pdf/<name>.pdf with the project's tectonic. Figures:
- fates: fate of the bug-revealing tests per policy, three models (stacked bars);
- metrics: mutation score on buggy and correct programs beside bug evidence and fix-blocking, per policy;
- tradeoff: share of bug-revealing tests reported against share of correct-program failures falsely reported,
  for the triage variants (judge, judge with code, weaker specifications), keep-all and discard. The oracle-lock
  replay is not plotted: it rests on the change-mode classifier, whose recall is low (ICST review, 23 October);
- decision: break-even share of buggy programs p* = cF / (D + cF) against the relative cost c of a false report.
Colours: Okabe-Ito palette. Usage: python analysis/figures.py [--no-compile]
"""
import os
import csv
import re
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import final_numbers as fn  # noqa: E402

# The TeX engine: tectonic on PATH, or the path in GBE_TECTONIC (this machine keeps it outside the repository).
TECTONIC = Path(os.environ.get('GBE_TECTONIC', 'tectonic'))
OUT = ROOT / 'figures'
RUNS = {'phase2_qwen25_code': 'Qwen2.5-Coder 7B', 'phase2_qwen35_code': 'Qwen3.5 9B', 'phase2_gemma4_code': 'Gemma 4 12B'}
MODEL_COLOUR = {'phase2_qwen25_code': 'oiblue', 'phase2_qwen35_code': 'oivermillion', 'phase2_gemma4_code': 'oigreen'}
POLICIES = [('P1', 'discard'), ('P2', 'overwrite'), ('P3', 'free repair'), ('P4', 'triage')]
COLOURS = r"""\definecolor{oiblue}{HTML}{0072B2}
\definecolor{oivermillion}{HTML}{D55E00}
\definecolor{oigreen}{HTML}{009E73}
\definecolor{oiorange}{HTML}{E69F00}
\definecolor{oisky}{HTML}{56B4E9}
\definecolor{oipurple}{HTML}{CC79A7}
\definecolor{oigrey}{HTML}{999999}
"""
PREAMBLE = r"""\documentclass[border=2pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{libertine}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{groupplots}
\usetikzlibrary{calc}
\begin{document}
\input{%s.tikz}
\end{document}
"""


def pct(x):
    return f'{100 * x:.1f}'


def fig_fates(data):
    fates = [('INVERTED', 'inverted (now asserts the bug)', 'oivermillion'), ('NEUTRALIZED', 'neutralized (passes on both versions)', 'oiorange'),
             ('DROPPED', 'dropped', 'oigrey'), ('REPORTED', 'reported as a likely bug', 'oigreen')]
    lines = [COLOURS, r'\begin{tikzpicture}', r'\begin{groupplot}[group style={group size=3 by 1, horizontal sep=14pt, yticklabels at=edge left},',
             r'  width=5.4cm, height=3.4cm, xmin=0, xmax=100, enlarge y limits=0.18,',
             r'  ytick={1,2,3,4}, yticklabels={triage, free repair, overwrite, discard}, y dir=normal,',
             r'  xtick={0,50,100}, minor xtick={25,75}, xmajorgrids, xminorgrids, grid style={gray!25}, xlabel style={font=\footnotesize},',
             r'  tick label style={font=\scriptsize}, title style={font=\footnotesize, yshift=-4pt},',
             r'  legend style={font=\footnotesize, draw=none, legend columns=4, /tikz/every even column/.append style={column sep=8pt}},',
             r'  area legend]']
    for run, name in RUNS.items():
        rows = data[run]
        extra = {'phase2_qwen25_code': ', legend to name=fateslegend', 'phase2_qwen35_code': r', xlabel={\% of bug-revealing tests}'}.get(run, '')
        lines.append(r'\nextgroupplot[title={%s}, xbar stacked, bar width=7pt%s]' % (name, extra))
        for fate, label, colour in fates:
            coords = []
            for y, (p, _) in zip((4, 3, 2, 1), POLICIES):
                rev = [r for r in rows if r['stage'] == p and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS']
                coords.append(f'({pct(sum(r["fate"] == fate for r in rev) / len(rev))},{y})')
            lines.append(r'\addplot[fill=%s, draw=white, line width=0.3pt] coordinates {%s};' % (colour, ' '.join(coords)))
            if run == 'phase2_qwen25_code':
                lines.append(r'\addlegendentry{%s}' % label)
    lines += [r'\end{groupplot}', r'\node[anchor=north] at ($(group c2r1.south) + (0,-0.9cm)$) {\pgfplotslegendfromname{fateslegend}};',
              r'\end{tikzpicture}']
    return '\n'.join(lines)


def fig_metrics():
    with open(ROOT / 'review' / 'out' / 'rq3_units.csv', encoding='utf-8') as fh:
        units = list(csv.DictReader(fh))
    # Buggy programs only: the paper's RQ2 compares the policies there (correct-program scores barely differ).
    series = [('mutation score', 'oiblue', lambda rs: [float(r['mutation_score']) for r in rs if r['condition'] == 'buggy' and r['mutation_score'] != '']),
              ('suites that keep or report the bug evidence', 'oigreen', lambda rs: [int(r['evidence']) for r in rs if r['condition'] == 'buggy']),
              ('suites that assert the bug', 'oivermillion', lambda rs: [int(r['fix_blocking']) for r in rs if r['condition'] == 'buggy'])]
    lines = [COLOURS, r'\begin{tikzpicture}',
             r'\begin{groupplot}[group style={group size=3 by 1, horizontal sep=6pt, yticklabels at=edge left},',
             r'  width=5.6cm, height=3.6cm, ymin=0, ymax=100, enlarge x limits=0.16,',
             r'  symbolic x coords={discard, overwrite, free repair, triage}, xtick=data,',
             r'  xticklabels={discard, over-\\write, free\\repair, triage}, xticklabel style={align=center, font=\scriptsize},',
             r'  yticklabel style={font=\scriptsize}, ylabel style={font=\footnotesize},',
             r'  title style={font=\footnotesize, yshift=-4pt}, ymajorgrids, grid style={gray!25},',
             r'  legend style={font=\footnotesize, draw=none, legend columns=3, /tikz/every even column/.append style={column sep=8pt}},',
             r'  area legend]']
    for run, name in RUNS.items():
        extra = r', ylabel={\%}, legend to name=metricslegend' if run == 'phase2_qwen25_code' else ''
        lines.append(r'\nextgroupplot[title={%s}, ybar=0pt, bar width=4.2pt, legend image code/.code={\draw[#1, draw=none] (0cm,-0.08cm) rectangle (0.3cm,0.12cm);}%s]' % (name, extra))
        for label, colour, pick in series:
            coords = []
            for p, pname in POLICIES:
                vals = pick([r for r in units if r['run'] == run and r['stage'] == p])
                coords.append(f'({pname},{pct(statistics.mean(vals))})')
            lines.append(r'\addplot[fill=%s, draw=none] coordinates {%s};' % (colour, ' '.join(coords)))
            if run == 'phase2_qwen25_code':
                lines.append(r'\addlegendentry{%s}' % label)
    lines += [r'\end{groupplot}', r'\node[anchor=north] at ($(group c2r1.south) + (0,-0.85cm)$) {\pgfplotslegendfromname{metricslegend}};',
              r'\end{tikzpicture}']
    return '\n'.join(lines)


def s4_points(run):
    text = (ROOT / 'runs' / 's4_judge_specs' / run / 'summary.md').read_text(encoding='utf-8')
    pts = {}
    for spec, a, b in re.findall(r'^\| (no_examples|signature_only) \| \d+ of \d+ \((\d+)%\) \| \d+ of \d+ \((\d+)%\)', text, re.M):
        pts[spec] = (int(b), int(a))
    return pts


def fig_tradeoff(data):
    marks = [('judge', 'judge (triage)', 'mark=*'), ('code', 'judge also sees the code', 'mark=square*'),
             ('no_examples', 'judge, docstring without examples', 'mark=triangle*'),
             ('signature_only', 'judge, signature only', 'mark=diamond*')]
    lines = [COLOURS, r'\begin{tikzpicture}',
             r'\begin{axis}[width=6.8cm, height=6.2cm, xmin=-4, xmax=104, ymin=-4, ymax=104,',
             r'  xlabel={failing tests of correct programs reported (\%)}, ylabel={bug-revealing tests reported (\%)},',
             r'  label style={font=\footnotesize}, tick label style={font=\footnotesize}, grid=major, grid style={gray!20},',
             r'  legend style={font=\scriptsize, at={(0.5,-0.2)}, anchor=north, draw=none, legend columns=2,'
             r'  /tikz/every even column/.append style={column sep=6pt}}, legend cell align=left]',
             r'\addplot[only marks, mark=o, mark size=2.6pt, black] coordinates {(0,0)};',
             r'\addlegendentry{discard or overwrite}',
             r'\addplot[only marks, mark=x, mark size=3pt, black, thick] coordinates {(100,100)};',
             r'\addlegendentry{report every failing test}']
    for key, label, mark in marks:
        lines.append(r'\addlegendimage{only marks, %s, black}' % mark)
        lines.append(r'\addlegendentry{%s}' % label)
    for run, name in RUNS.items():
        lines.append(r'\addlegendimage{line width=2pt, %s}' % MODEL_COLOUR[run])
        lines.append(r'\addlegendentry{%s}' % name)
    for run in RUNS:
        rows = data[run]
        groups = fn.by_pair(rows)
        rev4 = lambda r: r['stage'] == 'P4' and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS'
        fixed_judged = lambda r: r['stage'] == 'P4' and r['condition'] == 'fixed' and r['judge_verdict'] != ''
        pts = {
            'judge': (fn.boot(groups, fn.ratio(lambda r: r['final_status'] == 'QUARANTINED', fixed_judged))[0],
                      fn.boot(groups, fn.ratio(lambda r: r['fate'] == 'REPORTED', rev4))[0]),
            'code': (fn.boot(groups, fn.ratio(lambda r: r['judge_with_code_verdict'] not in ('', 'TEST_WRONG'), fixed_judged))[0],
                     fn.boot(groups, fn.ratio(lambda r: r['judge_with_code_verdict'] not in ('', 'TEST_WRONG'),
                                              lambda r: rev4(r) and r['judge_verdict'] != ''))[0])}
        pts = {k: (100 * x, 100 * y) for k, (x, y) in pts.items()}
        pts.update(s4_points(run))
        for key, _, mark in marks:
            x, y = pts[key]
            lines.append(r'\addplot[only marks, %s, mark size=2.2pt, %s, fill opacity=0.85] coordinates {(%.1f,%.1f)};'
                         % (mark, MODEL_COLOUR[run], x, y))
    lines += [r'\end{axis}', r'\end{tikzpicture}']
    return '\n'.join(lines)


def fig_decision(data):
    lines = [COLOURS, r'\begin{tikzpicture}',
             r'\begin{axis}[width=7.4cm, height=5.2cm, xmin=0, xmax=1, ymin=0, ymax=50, domain=0:1, samples=101,',
             r'  xlabel={cost of a false report relative to a missed bug, $c$},',
             r'  ylabel={break-even share of buggy programs $p^*$ (\%)},',
             r'  label style={font=\footnotesize}, tick label style={font=\footnotesize}, grid=major, grid style={gray!20},',
             r'  legend style={font=\scriptsize, at={(0.03,0.97)}, anchor=north west, draw=none, fill=white, fill opacity=0.8, text opacity=1},',
             r'  legend cell align=left]']
    for run, name in RUNS.items():
        flags = fn.program_flags(data[run], run)
        D = fn.program_rate(flags, 'buggy', lambda f: f['evidence_P4'])[0]
        F = fn.program_rate(flags, 'fixed', lambda f: f['false_report'])[0]
        lines.append(r'\addplot[%s, thick, no marks] {100*x*%.4f/(%.4f + x*%.4f)};' % (MODEL_COLOUR[run], F, D, F))
        lines.append(r'\addlegendentry{%s ($D$ = %.0f\%%, $F$ = %.0f\%%)}' % (name, 100 * D, 100 * F))
    lines += [r'\node[font=\scriptsize, anchor=west] at (axis cs:0.03,22) {triage costs less};',
              r'\node[font=\scriptsize, anchor=north east] at (axis cs:0.98,7) {silent repair costs less};',
              r'\end{axis}', r'\end{tikzpicture}']
    return '\n'.join(lines)


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / 'pdf').mkdir(exist_ok=True)
    data = {run: fn.rows(run) for run in RUNS}
    figures = {'fates': fig_fates(data), 'metrics': fig_metrics(), 'tradeoff': fig_tradeoff(data), 'decision': fig_decision(data)}
    for name, body in figures.items():
        (OUT / f'{name}.tikz').write_text(body + '\n', encoding='utf-8')
        (OUT / f'{name}.tex').write_text(PREAMBLE % name, encoding='utf-8')
        if '--no-compile' not in sys.argv:
            res = subprocess.run([str(TECTONIC), '-X', 'compile', f'{name}.tex', '--outdir', 'pdf'], cwd=OUT,
                                 capture_output=True, text=True, encoding='utf-8', errors='replace')
            print(name, 'ok' if res.returncode == 0 else 'FAILED\n' + res.stderr[-2000:])


if __name__ == '__main__':
    main()
