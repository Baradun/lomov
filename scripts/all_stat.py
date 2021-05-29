#!/usr/bin/python3

import os
import sys
from pathlib import Path
from pprint import pprint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import graphs.stat as gs

DATA_DIR = os.getenv("METHODS_DATA_DIR", "data")
OUT_DIR = os.getenv("METHODS_GRAPH_DIR", "all_graphs")
METHODS = ["M2", "M4", "M6", "CF4", "CF4:3"]
DF_COLS = {'RANGE': 1, 'START': 2, 'END': 3, 'METHOD': 4, 'STEP': 5,
           'PROB': 6, 'TIME': 7}
REF_METHOD = "M6"
REF_STEP = 1e-10
EDGE_VALUE = 1e-8


def collect_data():
    #data = pd.DataFrame()
    data = pd.DataFrame()

    for i in os.listdir(DATA_DIR):
        if i.startswith('host'):
            data_t = pd.DataFrame(gs.collect_data(
                Path(DATA_DIR) / str(i) / 'data'))
            data_t['host'] = i
            data = data.append(data_t, ignore_index=True)
    return data


def gen_gp_dat(data, graf_type=0):

    rngs = pd.unique(data['range'])
    hosts = pd.unique(data['host'])
    steps = pd.unique(data['step'])

    # x = steps; y = err
    if graf_type == 0:
        data_t = data.copy()
        data_t.insert(8, 're', 0)
        data_t.insert(9, 'sp', 0)
        for h in hosts:
            for r in rngs:
                sel = (data['host'] == h) & (data['range'] == r)
                max_time = data[sel]['time'].max()
                data_t.loc[sel, 'rt'] = data[sel]['time'] / max_time

        for r in rngs:
            with open(Path(OUT_DIR) / f'gt0_average_{r}.csv', 'w') as d:
                d.write('step,')
                for h in hosts:
                    for m in METHODS:
                        d.write(f'{m}_{h},')
                d.write('\n')


        for r in rngs:
            with open(Path(OUT_DIR) / f'gt0_average_{r}.csv', 'a') as d:
                for s in steps:
                    d.write(f'{s},')
                    for h in hosts:
                        for m in METHODS:
                            # d.write('{m}_host')
                            sel = (data_t['range'] == r) & (
                                data_t['step'] == s) & (
                                data_t['method'] == m) & (
                                    data_t['host'] == h)
                            value = data_t[sel]['rt'].sum()
                            count = data_t[sel]['rt'].count()
                            d.write(f'{value/count},')
                    d.write('\n')
                d.write('\n\n')
        
        for r in rngs:
            with open(Path(OUT_DIR) / f'gt0_average_{r}.csv', 'r') as d:
                clt_data = pd.read_csv(d)
                clt_data.plot(clt_data.step, )
                plt.show()
        
    # x = step; y = time
    if graf_type == 1:
        for rng in rngs:
            steps = pd.unique(data[data['range'] == rng]['step'])
            for stp in steps:
                print(stp, end=' ')
                # for m in METHODS:
                for hst in hosts:
                    rng_s = data[data['host'] == hst][data['range']
                                                      == rng].sort_values('step')
                    steps = rng_s['step'].unique()
                    m2_t = rng_s[rng_s['method'] == 'M2']['time'].to_numpy()
                    m4_t = rng_s[rng_s['method'] == 'M4']['time'].to_numpy()
                    m6_t = rng_s[rng_s['method'] == 'M6']['time'].to_numpy()
                    cf4_t = rng_s[rng_s['method'] == 'CF4']['time'].to_numpy()
                    cf43_t = rng_s[rng_s['method'] ==
                                   'CF4:3']['time'].to_numpy()

                    # gp_dat.write("# STEP\tEXECUTION TIME\n")
                    # gp_dat.write("#       M2\tM4\tM6\tCF4\tCF4:3\n")
                    for k, step in enumerate(steps):
                        print(f"\t{m2_t[k]}\t{m4_t[k]}\t{m6_t[k]}" +
                              f"\t{cf4_t[k]}\t{cf43_t[k]}\n")
                print()
            print('\n\n\n')

    # x = step; y = time
    if graf_type == 2:
        data_t = data.copy()
        data_t.insert(8, 'rt', 0)
        for h in hosts:
            for r in rngs:
                sel = (data['host'] == h) & (data['range'] == r)
                max_time = data[sel]['time'].max()
                data_t.loc[sel, 'rt'] = data[sel]['time'] / max_time

        # for rng in rngs:
        #     for host in hosts:
        #         for mth in METHODS:
        #             sel = (data_t['host'] == host) & (data_t['range'] == rng)
        #             x = data_t[sel]

        # for r in rngs:
        #     for s in steps:
        #         for m in METHODS:
        #             sel = (data_t['range'] == r) & (
        #                 data_t['step'] == s) & (data_t['method'] == m)
        #             value = data_t[sel]['rt'].sum()
        #             count = data_t[sel]['rt'].count()
        #             d.write(f'\t{value/count} ')
        for r in rngs:
            with open(Path(OUT_DIR) / f'gt2_collected_{r}.csv', 'w') as d:
                d.write('step,')
                for h in hosts:
                    for m in METHODS:
                        d.write(f'{m}_{h},')
                d.write('\n')


        for rng in rngs:
            with open(Path(OUT_DIR) / f'gt2_collected_{rng}.csv', 'a') as d:
                # d.write(f'{rng}\n\n')
                steps = pd.unique(data_t[data_t['range'] == rng]['step'])
                for stp in steps:
                    d.write(f'{stp},')
                    # for m in METHODS:
                    for hst in hosts:
                        sel = (data_t['host'] == hst) & (
                            data_t['range'] == rng)
                        rng_s = data_t[sel]
                        rng_s = rng_s[rng_s['step'] == stp]

                        m2_t = rng_s[rng_s['method'] ==
                                     'M2']['rt'].to_numpy()
                        m4_t = rng_s[rng_s['method'] ==
                                     'M4']['rt'].to_numpy()
                        m6_t = rng_s[rng_s['method'] ==
                                     'M6']['rt'].to_numpy()
                        cf4_t = rng_s[rng_s['method'] ==
                                      'CF4']['rt'].to_numpy()
                        cf43_t = rng_s[rng_s['method'] ==
                                       'CF4:3']['rt'].to_numpy()
                        d.write(f"{m2_t[0]},{m4_t[0]},{m6_t[0]}," +
                                f"{cf4_t[0]},{cf43_t[0]},")
                    d.write('\n')

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
