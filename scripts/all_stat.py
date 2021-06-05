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

    # if not os.path.isdir(Path(DATA_DIR)):
    #     print(f"We expect data to be in '{DATA_DIR}' directory, " +
    #           "but it is missing!")
    #     sys.exit(1)

    # if not os.path.isdir(Path(OUT_DIR)):
    #     try:
    #         os.mkdir(Path(OUT_DIR))
    #     except FileExistsError as err:
    #         print(f"We need directory '{OUT_DIR}' to store generated file but " +
    #               f"we got error while trying to create one: {err}")
    #     except:
    #         print("Unexpected error: ", sys.exc_info()[0])
    #         raise

    # data = gs.collect_all_data("data")

    data_to_graf = gs.gen_gp_dat(OUT_DIR, 3)
    
    print(data_to_graf)
    with open(Path(OUT_DIR) / ' data_to_graf.csv', 'w') as d:
        d.write( data_to_graf.to_csv())
    #gen_gp_dat(req_data, 0)
