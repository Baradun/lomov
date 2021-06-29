#!/usr/bin/env python3

"""
Collect data from dat files from 'methods.py' run and output data files for
plotting by gnuplot. Also do some statistical calculations on data.
"""

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REF_METHOD = "M6"
REF_STEP = 1e-10
METHODS = ["M2", "M4", "M6", "CF4", "CF4:3"]


def info(content):
    """Extract and return a list of necessary parameters from a content.
    """

    cntn = content.split()
    start = float(cntn[cntn.index('start') + 2])
    end = float(cntn[cntn.index('end') + 2])
    step = float(cntn[cntn.index('step') + 2])
    time = float(cntn[cntn.index('time') + 2])
    P = float(cntn[cntn.index('P') + 2])

    return start, end, step, time, P


def collect_data(DATA_DIR):
    """Get data from files in data directory.

    Also do some statistical calculations.
    """

    data_t = {k: [] for k in METHODS}
    for m in METHODS:
        tt = dict()
        met = []
        for f in Path(DATA_DIR).glob(m + '*.dat'):
            with open(f, 'r') as fil:
                data = fil.read()
                # Possible issue: if for some reason file exists but doesn't
                # contain necessary information, for example, file was created
                # before data were written and the process was killed, or if
                # file was written by other programs with other parameter
                # listing style.
                start, end, step, time, P = info(data)
                idx = f"{start},{end}_{step}"
                if idx not in tt:
                    tt[idx] = [float(time), 1]
                    met.append(
                        {
                            'start': start,
                            'end': end,
                            'step': step,
                            'prob': P,
                            'time': 0.0
                        }
                    )
                    continue
                tt[idx][0] = tt[idx][0] + float(time)
                tt[idx][1] = tt[idx][1] + 1
        for itm in met:
            idx = f"{itm['start']},{itm['end']}_{itm['step']}"
            itm['time'] = tt[idx][0] / tt[idx][1]
        data_t[m] = met

    data_c = []
    for m in METHODS:
        for el in data_t[m]:
            data_c.append(
                {
                    "range": f"({el['start']},{el['end']})",
                    "start": el['start'],
                    "end": el['end'],
                    "method": m,
                    "step": el['step'],
                    "prob": el['prob'],
                    "time": el['time']
                }
            )

    return data_c


def collect_all_data(DATA_DIR):
    #data = pd.DataFrame()
    data = pd.DataFrame()

    for i in os.listdir(DATA_DIR):
        if i.startswith('host'):
            data_t = pd.DataFrame(collect_data(
                Path(DATA_DIR) / str(i) / 'data'))
            data_t['host'] = i
            data = data.append(data_t, ignore_index=True)
    return data


def required_data(DATA_DIR):
    data = collect_all_data(DATA_DIR)

    data_t = data.copy()
    data_t.insert(8, 'rt', 0)
    data_t.insert(9, 'frt', 0)
    data_t.insert(10, 're', 0)
    data_t.insert(10, 'fre', 0)
    data_t.insert(11, 'sp', 0)
    

    rngs = pd.unique(data_t['range'])
    hosts = pd.unique(data_t['host'])
    steps = pd.unique(data_t['step'])
    methods = pd.unique(data_t['method'])

    # filling the 'rt' column

    for h in hosts:
        for r in rngs:
            sel = (data_t['host'] == h) & (data_t['range'] == r)
            max_time = data_t[sel]['time'].max()
            data_t.loc[sel, 'rt'] = data_t[sel]['time'] / max_time

    # filling the 'frt' column
    for r in rngs:
        for s in steps:
            for m in methods:
                sel = (data_t['range'] == r) & (
                    data_t['step'] == s) & (data_t['method'] == m)
                ts = data_t[sel]['rt'].sum()
                tc = data_t[sel]['rt'].count()
                mid = ts / tc
                data_t.loc[sel, 'frt'] =  (data_t[sel]['rt'] - mid) / mid




    # filling the 're' column

    for h in hosts:
        for r in rngs:
            sel = (data_t['host'] == h) & (data_t['range'] == r) & (
                data_t['step'] == REF_STEP) & (data_t['method'] == REF_METHOD)
            base_prob = data_t[sel]['prob'].to_numpy()[0]
            for m in methods:
                sel = (data_t['host'] == h) & (
                    data_t['range'] == r) & (data_t['method'] == m) 
                data_t.loc[sel, 're'] = (
                    data_t[sel]['prob'] - base_prob) / base_prob
    
    
    # filling the 'fre' column
    for r in rngs:
        for s in steps:
            for m in methods:
                sel = (data_t['range'] == r) & (
                    data_t['step'] == s) & (data_t['method'] == m)
                ts = data_t[sel]['re'].sum()
                tc = data_t[sel]['re'].count()
                mid = ts / tc
                data_t.loc[sel, 'fre'] =  (data_t[sel]['re'] - mid) / mid


    # filling the 'sp' column
    for r in rngs:
        for s in steps:
            for m in methods:
                sel = (data_t['range'] == r) & (
                    data_t['step'] == s) & (data_t['method'] == m)
                ts = data_t[sel]['prob'].sum()
                tc = data_t[sel]['prob'].count()
                data_t.loc[sel, 'sp'] = ts / tc

    return data_t


def gen_gp_dat(OUT_DIR, types, methods=None, hosts=None, rngs=None):
    """Generate data files from results of program run.

    Data files are generated for each computed interval. They names are prefixed
    by graph type followed by range interval.

    Due to fact we don't know exact solution for evolution equation (and that
    would be intrinsically wrong as we could change profile function at our
    will) we use numeric methods to calculate the solution.

    There is good method named Magnus expansion (after Wilfred Magnus work [1])
    in different form (related to each other as much as Runge-Kutta methods).

    We suppose that more "sophisticated" method with smallest step should give
    more correct result (more significant digits).

    The first graph type (gt == 0) is aimed at that: to compare calculation made
    by different methods by means of relative error. The error itself is
    computed on base of value for given method (REF_METHOD) and step (REF_STEP).

    Next graph type (gt == 1) is about absolute execution time. It depends very
    strongly on host where data were calculated.

    That's why we also generate data for thrid graph type (gt == 2) which writes
    relative execution time for every methods using as base most time consuming
    method (it is selected from the input data) on an intelval.

    """
    if os.path.exists(Path(OUT_DIR) / 'collected_data.csv'):
        with open(Path(OUT_DIR) / 'collected_data.csv', 'r') as d:
            data = pd.read_csv(d)
    else: 
        data = required_data("data")
        with open(Path(OUT_DIR) / 'collected_data.csv', 'w') as d:
            d.write(data.to_csv())

    
    steps = pd.unique(data['step'])
    if rngs is None:
        rngs = pd.unique(data['range'])
    if hosts is None:
        hosts = pd.unique(data['host'])
    if methods is None:
        methods = pd.unique(data['method'])
    
    
    ret_data = pd.DataFrame()
    ret_data.insert(0, 'step', 0)
    ret_data.insert(1, 'range', 0)
    
    print(data)
    for r in rngs:
        ret_data = ret_data.append(pd.DataFrame({'step': steps, 'range': r}), ignore_index=True)
    


    index = 2
    for h in hosts:
        for m in methods:
            for t in types:
                cname = f'{m}_{h}_{t}'
                ret_data.insert(index, cname, 0 )
                index += 1
                for r in rngs:
                    for s in steps:
                        sel1 = (data['host'] == h) & (data['method'] == m) &  (data['range'] == r) &  (data['step'] == s)
                        sel2 = (ret_data['range'] == r) & (ret_data['step'] == s)
                        ret_data.loc[sel2, cname] = data[sel1][t].to_numpy()[0]

    return ret_data


