#!/usr/bin/env python3

import json
import os
import random
import sys
from pathlib import Path

methods = ['M2', 'M4', 'M6', 'CF4', 'CF4:3']
steps = [1e-10]
start = 0.1
end = 0.5
params = [
    {
        'e': 3,
        'v0': 6.5956e4,
        'n': 10.54
    },
    {
        'e': 3,
        'v0': 6.5956e4,
        'n': 10.54
    },
    {
        'e': 3,
        'v0': 6.5956e4,
        'n': 10.54
    },
    {
        'e': 3,
        'v0': 6.5956e4,
        'n': 10.54
    },

]


JSON_DIR = Path('methods')

if not os.path.isdir(JSON_DIR):
    try:
        os.mkdir(JSON_DIR)
    except FileExistsError as err:
        print(f'We need directory "{JSON_DIR}" to store generated file but we \
got error while trying to create one: {err}')
    except:
        print('Unexpected error: ', sys.exc_info()[0])
        raise

rngs = []

delta = (end - start)/len(params) 
end = start
for i in params:
    end += delta
    rngs.append((start, end))
    start = end

print(rngs)

work = []

for m in methods:
    for r in rngs:
        for s in steps:
            for i, _ in enumerate(params):
                work.append({
                    'method': f'{m}',
                    'start': r[0],
                    'end': r[1],
                    'step': s,
                    'e': params[i].get('e'),
                    'v0': params[i].get('v0'),
                    'n': params[i].get('n')})

shfld = random.sample(work, k=len(work))

with open(JSON_DIR / 'work.json', 'w') as f:
    json.dump({'work': shfld}, f, indent='  ')
with open(JSON_DIR / 'work-do.json', 'w') as f:
    json.dump({'work': work}, f, indent='  ')