# C2 adjudication: instructions

You and Claude labelled the same 100 pull requests. In 39 of them the labels differ. For each of those, decide
the final label. The agreement score from before (kappa 0.57) is already fixed and is reported as it is; the
final labels are the ones the paper counts.

## Files

- `c2_adjudication.csv` (open in Excel): one row per case. It shows your label and note, Claude's label and
  one-line reason, and three empty columns to fill.
- `C2_ADJUDICATION_READER.html` (double-click to open): the same cases as cards, with the changed asserts, the
  description, the code change and both labels side by side. Easier to read than the CSV.
- `C2_LABEL_GUIDE.html`: the label rules, unchanged.

## What to do, per row

1. Read the case in the reader, then both labels and reasons.
2. Fill `FINAL WHY` with one letter (I, W, E, M or U) and `FINAL SAYS` with Y or N.
   - Keep your label, take Claude's, or choose a third one if seeing both changes your view.
   - Only one of the two may differ in a row (see "Differ on" in the reader); still fill both FINAL columns,
     copying the label you both gave for the other one.
3. Optional: a short `final note`, for example why you kept your label.
4. Save the file as CSV with the same name when you are done (you can stop and continue later).

## How to decide

- Use the same rules as before (`C2_LABEL_GUIDE.html`). A reason that points to something concrete in the pull
  request (a line in the description, a comment next to the assert, the code change) is stronger than a
  general impression.
- U stays a valid final answer when the case really cannot be decided from the pull request.
- There is no need to agree with Claude. If you think Claude's reason is wrong, keep your label.

About 1 minute per row, so 30 to 45 minutes for all 39.
