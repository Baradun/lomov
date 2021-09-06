#!/usr/bin/python3

import os
import sys
from pathlib import Path

# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import graphs.stat as gs

DATA_DIR = os.getenv("METHODS_DATA_DIR", "data")
OUT_DIR = os.getenv("METHODS_GRAPH_DIR", "all_graphs")


def mrk():
    m = "*HsXv^2348"*20
    for i in m:
        yield i


if __name__ == '__main__':

    methods = ["CF4"]
    host = ['host#b9ec88ad']
    data_to_graf = gs.gen_dat(
        OUT_DIR, DATA_DIR, ['frt', ], hosts=host, rngs=['(0.1,0.3)'])
    print(data_to_graf)

    data_t = data_to_graf.sort_values(by='step')

    m = mrk()
    for i in data_to_graf.columns.values.tolist():
        if i.find('host') >= 0:
            fm = next(m)
            #plt.plot(data_t['step'], np.abs(data_t[i]), f'{fm}-', label=str(i))

    tag = methods[0]
    # plt.title(tag)
    # plt.legend(fontsize=8)
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.savefig(f'plot_{tag}.pdf')
    # plt.show()

    with open(Path(OUT_DIR) / 'data_to_graf.csv', 'w') as d:
        d.write(data_to_graf.to_csv())
    #gen_gp_dat(req_data, 0)
