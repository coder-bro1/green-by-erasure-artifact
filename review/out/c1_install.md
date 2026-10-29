# C1 attrition, steps 2 and 3

Computed by `analysis/c1_install.py` (docs/C1_PROTOCOL.md, section 9 changes 1 to 3). Bugs in selection order;
stop at 8 eligible per project or 30 in all; a project leaves after its first 3 attempts fail step 2.

| Project | Steps 1+4 | Attempted | Step 2 fails | Step 3 fails | Eligible | Not tried |
|---|---:|---:|---:|---:|---:|---:|
| spacy | 5 | 5 | 4 | 0 | 1 | 0 |
| cookiecutter | 2 | 2 | 0 | 0 | 2 | 0 |
| httpie | 2 | 2 | 0 | 0 | 2 | 0 |
| sanic | 3 | 3 | 1 | 0 | 2 | 0 |
| pandas | 73 | 8 | 0 | 0 | 8 | 65 |
| tornado | 9 | 8 | 0 | 0 | 8 | 1 |
| ansible | 6 | 3 | 3 | 0 | 0 | 3 |
| luigi | 24 | 7 | 0 | 0 | 7 | 17 |
| thefuck | 20 | 0 | 0 | 0 | 0 | 20 |
| keras | 23 | 0 | 0 | 0 | 0 | 23 |
| matplotlib | 20 | 0 | 0 | 0 | 0 | 20 |
| tqdm | 5 | 0 | 0 | 0 | 0 | 5 |
| scrapy | 24 | 0 | 0 | 0 | 0 | 24 |
| black | 11 | 0 | 0 | 0 | 0 | 11 |
| youtube-dl | 27 | 0 | 0 | 0 | 0 | 27 |
| PySnooper | 1 | 0 | 0 | 0 | 0 | 1 |
| fastapi | 11 | 0 | 0 | 0 | 0 | 11 |
| all | 266 | 38 | 8 | 0 | 30 | 228 |

## Per attempted bug

| Bug | Python | Step 2 | Step 3 | Minutes |
|---|---|---|---|---:|
| spacy-2 | 3.7.7 | pass | pass | 7 |
| spacy-6 | 3.7.7 | fail: the buggy checkout cannot import the project or a dependency |  | 3 |
| spacy-4 | 3.8.3 | fail: the buggy checkout cannot import the project or a dependency |  | 3 |
| spacy-1 | 3.7.7 | fail: the buggy checkout cannot import the project or a dependency |  | 3 |
| spacy-5 | 3.7.7 | fail: the buggy checkout cannot import the project or a dependency |  | 3 |
| cookiecutter-1 | 3.6.8 | pass | pass | 2 |
| cookiecutter-3 | 3.6.8 | pass | pass | 3 |
| httpie-3 | 3.7.3 | pass | pass | 2 |
| httpie-4 | 3.7.3 | pass | pass | 2 |
| sanic-1 | 3.8.3 | pass | pass | 18 |
| sanic-3 | 3.8.3 | pass | pass | 15 |
| sanic-4 | 3.8.3 | fail: the fixed checkout cannot import the project or a dependency |  | 14 |
| pandas-168 | 3.8.3 | pass | pass | 17 |
| pandas-23 | 3.8.3 | pass | pass | 6 |
| pandas-119 | 3.8.3 | pass | pass | 12 |
| pandas-127 | 3.8.3 | pass | pass | 11 |
| pandas-58 | 3.8.3 | pass | pass | 6 |
| pandas-161 | 3.8.3 | pass | pass | 15 |
| pandas-69 | 3.8.3 | pass | pass | 11 |
| pandas-162 | 3.8.3 | pass | pass | 15 |
| tornado-14 | 3.7.0 | pass | pass | 0 |
| tornado-4 | 3.7.0 | pass | pass | 0 |
| tornado-5 | 3.7.0 | pass | pass | 0 |
| tornado-8 | 3.7.0 | pass | pass | 1 |
| tornado-3 | 3.7.0 | pass | pass | 0 |
| tornado-2 | 3.7.0 | pass | pass | 1 |
| tornado-11 | 3.7.0 | pass | pass | 1 |
| tornado-13 | 3.7.0 | pass | pass | 1 |
| ansible-15 | 3.6.8 | fail: the buggy checkout cannot import the project or a dependency |  | 5 |
| ansible-1 | 3.6.8 | fail: the buggy checkout cannot import the project or a dependency |  | 2 |
| ansible-3 | 3.6.8 | fail: the buggy checkout cannot import the project or a dependency |  | 2 |
| luigi-4 | 3.8.3 | pass | pass | 12 |
| luigi-25 | 3.8.3 | pass | pass | 16 |
| luigi-20 | 3.8.3 | pass | pass | 16 |
| luigi-28 | 3.8.3 | pass | pass | 16 |
| luigi-33 | 3.8.3 | pass | pass | 17 |
| luigi-31 | 3.8.3 | pass | pass | 16 |
| luigi-21 | 3.8.3 | pass | pass | 16 |
