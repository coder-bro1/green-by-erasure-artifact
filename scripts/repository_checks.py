"""Read-only repository checks restricted to this project and parent git status."""
import json
import re
import subprocess

from gbe.util import ROOT, write_json


def git(*args,cwd=ROOT):
    return subprocess.check_output(['git',*args],cwd=cwd,text=True,encoding='utf-8',errors='replace').strip()


messages=git('log','--format=%B')
patterns=[r'AIza[0-9A-Za-z_-]{35}',r'sk-[A-Za-z0-9]{20,}',r'api[_-]?key\s*=']
hits=[]
for path in ROOT.rglob('*'):
    if any(part in ('.git','.venv','.scratch','__pycache__','downloads','.ollama-models') for part in path.relative_to(ROOT).parts):
        continue
    if path.is_file() and path.suffix.lower() in ('.py','.txt','.md','.json','.jsonl','.csv','.ps1','.toml','.log'):
        content=path.read_text(encoding='utf-8-sig',errors='replace')
        for pattern in patterns:
            if re.search(pattern,content):
                hits.append({'path':str(path.relative_to(ROOT)),'pattern':pattern})
history=git('log','-p')
history_hits=[pattern for pattern in patterns if re.search(pattern,history)]
parent=git('status','--short',cwd=ROOT.parent)
protocol=(ROOT/'docs/REVIEW_PROTOCOL.md').read_text(encoding='utf-8')
baseline=protocol.rsplit('```',2)[1].strip()
astra=[]
identifier_pattern='mutation_'+'analyzer|Mut'+'Py|mut'+r'\.py'
for directory in ('src','scripts','tests'):
    for path in (ROOT/directory).rglob('*.py'):
        if re.search(identifier_pattern,path.read_text(encoding='utf-8')):
            astra.append(str(path.relative_to(ROOT)))
result={'G2':{'pass':not re.search('Co-Authored'+'-By|Generated '+'with',messages,re.I)},
        'G3':{'pass':all(len(body.split())>=25 for body in git('log','--format=%b%x1e').split('\x1e') if body.strip()),
              'log':git('log','--format=%h %s%n%b%n---')},
        'G4':{'pass':not hits and not history_hits,'file_hits':hits,'history_hits':history_hits},
        'G5':{'pass':parent==baseline,'actual':parent,'expected':baseline},
        'G6':{'pass':not astra,'distinctive_identifier_matches':astra,
              'note':'Forbidden parent source files were never read; long-passage comparison is intentionally unavailable.'}}
write_json(ROOT/'runs/setup/repository_checks.json',result)
print(json.dumps(result,indent=2))
