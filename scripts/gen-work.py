#!/usr/bin/env python

"""
Generate json files to get data for statistics on used methods.
"""

import json
import os
import sys
from pathlib import Path
import random

methods = [ "M2", "M4", "M6", "CF4" , "CF4:3" ]
steps = [ 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10 ]
rngs = [ (0.1, 0.15), (0.1, 0.2), (0.1, 0.3) ]

work = []

JSON_DIR = Path("methods")

if not os.path.isdir(JSON_DIR):
    try:
        os.mkdir(JSON_DIR)
    except FileExistsError as err:
        print(f"We need directory '{JSON_DIR}' to store generated file but we \
                got error while trying to create one: {err}")
    except:
        print("Unexpected error: ", sys.exc_info()[0])
        raise

for r in rngs:
    for m in methods:
        for s in steps:
            work.append({
                "method" : f"{m}",
                "start" : r[0],
                "stop" : r[1],
                "step": s})

shfld = random.sample(work, k=len(work))

with open(JSON_DIR / "work.json", "w") as f:
    json.dump({ "work" : shfld }, f, indent="  ")
with open(JSON_DIR / "work-do.json", "w") as f:
    json.dump({ "work" : work }, f, indent="  ")
