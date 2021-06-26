#!/usr/bin/python3

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import graphs.stat as gs

DATA_DIR = os.getenv("METHODS_DATA_DIR", "data")
OUT_DIR = os.getenv("METHODS_GRAPH_DIR", "all_graphs")


if __name__ == '__main__':

    methods=['CF4:3']
    data_to_graf = gs.gen_gp_dat(OUT_DIR, ['re'], methods=methods, rngs=['(0.1,0.3)'], )
    print(data_to_graf)

    data_t = data_to_graf.sort_values(by='step')

    for i in data_to_graf.columns.values.tolist():
        if i.find('_') >= 0:
            plt.plot(data_t['step'], data_t[i], '*-')

    plt.title(methods)
    plt.xscale("log")
    plt.yscale("log")
    plt.savefig('plot.pdf')
    plt.show()

    with open(Path(OUT_DIR) / ' data_to_graf.csv', 'w') as d:
        d.write(data_to_graf.to_csv())
    #gen_gp_dat(req_data, 0)
