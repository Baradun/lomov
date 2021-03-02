#!/usr/bin/env python

import json
import os
from pathlib import Path
import random

methods = [ "M2", "M4", "M6", "CF4" , "CF4:3" ]
steps = [ 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10 ]
rngs = [ (0.1, 0.15), (0.1, 0.2), (0.1, 0.3) ]

work = []

json_dir = Path("methods")

## We didn't handle the case when json_dir exists but not a directory.
if not os.path.isdir(json_dir):
    os.mkdir(json_dir)

for r in rngs:
    for m in methods:
        for s in steps:
            work.append({
                "method" : f"{m}",
                "start" : r[0],
                "stop" : r[1],
                "step": s})

shfld = random.sample(work, k=len(work))

with open(json_dir / "work.json", "w") as f:
    json.dump({ "work" : shfld }, f, indent="  ")
with open(json_dir / "work-do.json", "w") as f:
    json.dump({ "work" : work }, f, indent="  ")
