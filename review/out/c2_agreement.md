# C2 step 4: agreement between the two raters

Computed by `analysis/c2_agreement.py`. 76 of the 100 sampled agent pull requests (seed gbe-c2-labels-v2): those
still candidates after the authorship filter of 19 October (only the agent's own commits count). Rater A: the
first rater (Claude, labels made from the sheet alone). Rater B: the second rater (the user). Labels before
adjudication.

- WHY, five labels: observed agreement 72%, Cohen kappa 0.57.
- Possible erasure (E against the rest): observed agreement 92%, kappa 0.36.
- WHY on the 55 cases neither rater marked U: agreement 87%, kappa 0.72.
- SAYS TEST CHANGED: observed agreement 87%, kappa 0.51.

| Label | Rater A (Claude) | Rater B (user) |
|---|---:|---:|
| I | 46 | 39 |
| W | 8 | 5 |
| E | 5 | 5 |
| M | 8 | 8 |
| U | 9 | 19 |
| SAYS = Y | 11 | 13 |

Confusion matrix (rows rater A, columns rater B):

| A \ B | I | W | E | M | U |
|---|---:|---:|---:|---:|---:|
| I | 36 | 1 | 2 | 1 | 6 |
| W | 0 | 3 | 0 | 0 | 5 |
| E | 2 | 0 | 2 | 0 | 1 |
| M | 1 | 0 | 0 | 7 | 0 |
| U | 0 | 1 | 1 | 0 | 7 |
- Step 2 disclosure regex against rater A: 29 flagged, 9 of them labelled Y (precision 31%); 11 labelled Y, 9 flagged (recall 82%).
- Step 2 disclosure regex against rater B: 29 flagged, 11 of them labelled Y (precision 38%); 13 labelled Y, 11 flagged (recall 85%).

