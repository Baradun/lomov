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

#DATA_DIR = os.getenv("METHODS_DATA_DIR", "data")
#OUT_DIR = os.getenv("METHODS_GRAPH_DIR", "graphs")
METHODS = ["M2", "M4", "M6", "CF4", "CF4:3"]
DF_COLS = {'RANGE': 1, 'START': 2, 'END': 3, 'METHOD': 4, 'STEP': 5,
           'PROB': 6, 'TIME': 7}
REF_METHOD = "M6"
REF_STEP = 1e-10
EDGE_VALUE = 1e-8


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


def gen_gp_dat(data, OUT_DIR, graf_type=0):
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

    rngs = pd.unique(data['range'])

    # x = steps; y = err
    if graf_type == 0:
        for rng in rngs:
            c_rng = data[data['range'] == rng]
            sel = c_rng[c_rng['method'] == REF_METHOD]
            sel = sel[sel['step'] == REF_STEP]
            bas_prob = sel['prob'].to_numpy()[0]

            rng_s = c_rng.sort_values('step')
            steps = rng_s['step'].unique()
            m2_p = rng_s[rng_s['method'] == 'M2']['prob'].to_numpy()
            m4_p = rng_s[rng_s['method'] == 'M4']['prob'].to_numpy()
            m6_p = rng_s[rng_s['method'] == 'M6']['prob'].to_numpy()
            cf4_p = rng_s[rng_s['method'] == 'CF4']['prob'].to_numpy()
            cf43_p = rng_s[rng_s['method'] == 'CF4:3']['prob'].to_numpy()

            with open(Path(OUT_DIR) / f'gt0_{rng}.dat', 'w') as gp_dat:
                gp_dat.write("# STEP\tRELATIVE ERROR\tSURVIVAL PROBABILITY\n")
                gp_dat.write("#       M2\tM4\tM6\tCF4\tCF4:3\n")
                for k, step in enumerate(steps):
                    reM2 = abs(m2_p[k] - bas_prob) / bas_prob
                    reM4 = abs(m4_p[k] - bas_prob) / bas_prob
                    reM6 = abs(m6_p[k] - bas_prob) / bas_prob
                    reCF4 = abs(cf4_p[k] - bas_prob) / bas_prob
                    reCF43 = abs(cf43_p[k] - bas_prob) / bas_prob
                    # ### If a relative error equals to zero we will use some
                    # ### EDGE value
                    if reM2 == 0.0:
                        reM2 = EDGE_VALUE
                    if reM4 == 0.0:
                        reM4 = EDGE_VALUE
                    if reM6 == 0.0:
                        reM6 = EDGE_VALUE
                    if reCF4 == 0.0:
                        reCF4 = EDGE_VALUE
                    if reCF43 == 0.0:
                        reCF43 = EDGE_VALUE
                    gp_dat.write(f"{step}\t{reM2}\t{m2_p[k]}\t{reM4}\t" +
                                 f"{m4_p[k]}\t{reM6}\t{m6_p[k]}\t{reCF4}" +
                                 f"\t{cf4_p[k]}\t{reCF43}\t{cf43_p[k]}\n")

    # x = step; y = time
    if graf_type == 1:
        for rng in rngs:
            rng_s = data[data['range'] == rng].sort_values('step')
            steps = rng_s['step'].unique()
            m2_t = rng_s[rng_s['method'] == 'M2']['time'].to_numpy()
            m4_t = rng_s[rng_s['method'] == 'M4']['time'].to_numpy()
            m6_t = rng_s[rng_s['method'] == 'M6']['time'].to_numpy()
            cf4_t = rng_s[rng_s['method'] == 'CF4']['time'].to_numpy()
            cf43_t = rng_s[rng_s['method'] == 'CF4:3']['time'].to_numpy()

            with open(Path(OUT_DIR) / f'gt1_{rng}.dat', 'w') as gp_dat:
                gp_dat.write("# STEP\tEXECUTION TIME\n")
                gp_dat.write("#       M2\tM4\tM6\tCF4\tCF4:3\n")
                for k, step in enumerate(steps):
                    gp_dat.write(f"{step}\t{m2_t[k]}\t{m4_t[k]}\t{m6_t[k]}" +
                                 f"\t{cf4_t[k]}\t{cf43_t[k]}\n")

    # x = step; y = time
    if graf_type == 2:
        for rng in rngs:
            rng_s = data[data['range'] == rng].sort_values('step')
            max_time = rng_s['time'].max()

            steps = rng_s['step'].unique()
            m2_t = rng_s[rng_s['method'] == 'M2']['time'].to_numpy() \
                / max_time
            m4_t = rng_s[rng_s['method'] == 'M4']['time'].to_numpy() \
                / max_time
            m6_t = rng_s[rng_s['method'] == 'M6']['time'].to_numpy() \
                / max_time
            cf4_t = rng_s[rng_s['method'] == 'CF4']['time'].to_numpy() \
                / max_time
            cf43_t = rng_s[rng_s['method'] == 'CF4:3']['time'].to_numpy() \
                / max_time

            with open(Path(OUT_DIR) / f'gt2_{rng}.dat', 'w') as gp_dat:
                gp_dat.write("## STEP\tRELATIVE EXECUTION TIME\n")
                gp_dat.write("#       M2\tM4\tM6\tCF4\tCF4:3\n")
                for k, step in enumerate(steps):
                    gp_dat.write(f"{step}\t{m2_t[k]}\t{m4_t[k]}\t{m6_t[k]}" +
                                 f"\t{cf4_t[k]}\t{cf43_t[k]}\n")
    

    with open(Path(OUT_DIR) / 'collected_data.csv', 'w') as d:
        d.write(data.to_csv())


if __name__ == '__main__':

    if not os.path.isdir(Path(DATA_DIR)):
        print(f"We expect data to be in '{DATA_DIR}' directory, " +
              "but it is missing!")
        sys.exit(1)

    if not os.path.isdir(Path(OUT_DIR)):
        try:
            os.mkdir(Path(OUT_DIR))
        except FileExistsError as err:
            print(f"We need directory '{OUT_DIR}' to store generated file but " +
                    f"we got error while trying to create one: {err}")
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

    data = pd.DataFrame(collect_data())

    gen_gp_dat(data, 0)
    gen_gp_dat(data, 1)
    gen_gp_dat(data, 2)
