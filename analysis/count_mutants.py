import json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, 'src')
from gbe.benchmarks import download, program
CR = str(Path(sys.executable).with_name('cosmic-ray.exe'))
rows, _ = download()
out = {}
for r in rows:
    for v in ('fixed', 'buggy'):
        with tempfile.TemporaryDirectory() as d:
            Path(d, 'solution.py').write_text(program(r, v), encoding='utf-8')
            Path(d, 'cr.toml').write_text('[cosmic-ray]\nmodule-path = "solution.py"\ntimeout = 30.0\nexcluded-modules = []\ntest-command = "x"\n[cosmic-ray.distributor]\nname = "local"\n')
            subprocess.run([CR, 'init', 'cr.toml', 's.sqlite', '--force'], cwd=d, check=True, capture_output=True)
            dump = subprocess.run([CR, 'dump', 's.sqlite'], cwd=d, check=True, capture_output=True, text=True).stdout
            out[f"{r['task_id']}|{v}"] = sum(len(json.loads(l)[0]['mutations']) for l in dump.splitlines())
json.dump(out, open('.scratch/mutant_counts.json', 'w'), indent=0)
vals = sorted(out.values()); n = len(vals)
print('versions', n, 'total', sum(vals), 'mean', round(sum(vals)/n, 1), 'median', vals[n//2], 'max', vals[-1], 'min', vals[0])
