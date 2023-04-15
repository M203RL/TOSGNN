from pathlib import Path
import os
from tqdm import trange

cd = Path(__file__).parent.resolve()
file = 'Link.txt'
path = os.path.join(cd, file)


f = open(path, encoding = 'utf8')
filtered = 'filtered.txt'
txt = os.path.join(cd, filtered)
text = []
for line in f:
    text.append(line)

filtext = []
for i in trange(len(text)):
    if '《神魔之塔》' in text[i][0:6]:
        filtext.append(text[i])
        filtext.append(text[i+1])
        filtext.append(text[i+2])

open(txt, 'w').close()

with open(txt, 'w', encoding = 'utf8') as f:
    for line in filtext:
        f.write(f"{line}")
