import argparse
from gbe.report import summarize
from gbe.util import ROOT

parser = argparse.ArgumentParser()
parser.add_argument('--run-id', default='phase1_pilot')
args = parser.parse_args()
summarize(ROOT / 'runs' / args.run_id)
