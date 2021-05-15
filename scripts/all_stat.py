#!/usr/bin/python3

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = os.getenv("METHODS_DATA_DIR", "data")
OUT_DIR = os.getenv("METHODS_GRAPH_DIR", "all_graphs")
METHODS = ["M2", "M4", "M6", "CF4", "CF4:3"]
DF_COLS = {'RANGE': 1, 'START': 2, 'END': 3, 'METHOD': 4, 'STEP': 5,
           'PROB': 6, 'TIME': 7}
REF_METHOD = "M6"
REF_STEP = 1e-10
EDGE_VALUE = 1e-8


def collect_data():

    data = pd.DataFrame()
    for i in os.listdir(DATA_DIR):
        if i.startswith('host'):
            with open(DATA_DIR+'/' + i+'/graphs/collected_data.csv', 'r') as f:
                csv = pd.read_csv(
                    f,
                    usecols=['range',
                             'start',
                             'end',
                             'method',
                             'step',
                             'prob',
                             'time'])
                csv['host'] = i
                data = data.append(csv, ignore_index=True)

    return data


def gen_gp_dat(data, graf_type=0):

    rngs = pd.unique(data['range'])
    hosts = pd.unique(data['host'])

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
            steps = pd.unique(data[data['range'] == rng]['step'])
            for stp in steps:
                print(stp, end=' ')
                # for m in METHODS:
                for hst in hosts:
                    rng_s = data[data['host'] == hst][data['range'] == rng].sort_values('step')
                    steps = rng_s['step'].unique()
                    m2_t = rng_s[rng_s['method'] == 'M2']['time'].to_numpy()
                    m4_t = rng_s[rng_s['method'] == 'M4']['time'].to_numpy()
                    m6_t = rng_s[rng_s['method'] == 'M6']['time'].to_numpy()
                    cf4_t = rng_s[rng_s['method'] == 'CF4']['time'].to_numpy()
                    cf43_t = rng_s[rng_s['method'] == 'CF4:3']['time'].to_numpy()

                
                    #gp_dat.write("# STEP\tEXECUTION TIME\n")
                    #gp_dat.write("#       M2\tM4\tM6\tCF4\tCF4:3\n")
                    for k, step in enumerate(steps):
                        print(f"\t{m2_t[k]}\t{m4_t[k]}\t{m6_t[k]}" +
                                    f"\t{cf4_t[k]}\t{cf43_t[k]}\n")
                print()
            print('\n\n\n')


    # x = step; y = time
    if graf_type == 2:
        for rng in rngs:
            steps = pd.unique(data[data['range'] == rng]['step'])
            for stp in steps:
                print(stp, end=' ')
                # for m in METHODS:
                for hst in hosts:
                    rng_s = data[data['host'] == hst][data['range'] == rng].sort_values('step')
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

                    # print("## STEP\tRELATIVE EXECUTION TIME\n")
                    # print("#       M2\tM4\tM6\tCF4\tCF4:3\n")
                    for k, step in enumerate(steps):
                        print(f"\t{m2_t[m2_t['step'] = stp]}\t{m4_t[k]}\t{m6_t[k]}" +
                                f"\t{cf4_t[k]}\t{cf43_t[k]}", end=' ')
                print()
            print('\n\n\n')
    


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

    data = collect_data()
    print(data)
    gen_gp_dat(data, 2)
