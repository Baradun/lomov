#!/usr/bin/env python3

"""
Collect data from dat files from 'methods.py' run and output data files for
plotting by gnuplot. Also do some statistical calculations on data.
"""

import os
from datetime import date
from pathlib import Path

import pandas as pd

#from scripts.all_stat import STORE_DIR

REF_METHOD = "M6"
REF_STEP = 1e-10
METHODS = ["M2", "M4", "M6", "CF4", "CF4:3"]


class DataRefine():
    def __init__(self, storeDir: str, dataDir: str, data_ext=None):
        """
        Populate internal data structure with data located in storeDir/dataDir.
        """

        # Internal methods.

        # Truely "internal" method.
        def info(content):
            """
            Extract and return a list of necessary parameters from a content.
            """

            cntn = content.split()
            start = float(cntn[cntn.index('start') + 2])
            end = float(cntn[cntn.index('end') + 2])
            step = float(cntn[cntn.index('step') + 2])
            time = float(cntn[cntn.index('time') + 2])
            P = float(cntn[cntn.index('P') + 2])

            return start, end, step, time, P

        # Truely "internal" method.
        def collect_data(d):
            """
            Get data from .dat files in a directory.
            """

            r_data = []
            for f in Path(d).glob('*.dat'):
                with open(f, 'r') as fil:
                    tf = str(f)
                    run = tf[tf.rindex('_')+2:tf.find('.dat')]
                    method = tf[tf.rindex('/')+1:tf.index('_')]

                    data = fil.read()
                    start, end, step, time, P = info(data)
                    r_data.append(
                        {
                            "range": f"({start};{end})",
                            "start": start,
                            "end": end,
                            'run': run,
                            "method": method,
                            "step": step,
                            "prob": P,  # prob
                            "time": time
                        }
                    )
            return r_data

        def parse_adaptive(path: str) -> pd.DataFrame:

            def parse_range(range: str) -> str:
                range = range[1:len(range)-1]
                l = []

                if range.find(',') != -1:
                    range = range.split(',')
                else:
                    range = range.split('.')

                for i in range:
                    if i.find('.') != -1:
                        l.extend(i.split('.'))
                    else:
                        l.append(i)
                return f'({l[0]}.{l[1]};{l[2]}.{l[3]})'

            data_adapt = pd.DataFrame({
                'e': [],
                'range': [],
                'prob': [],
            })

            with open(Path(path) / 'adaptive.dat', 'r') as f:
                for l in f:
                    line = l.split()
                    data_adapt = data_adapt.append({
                        'e': line[0],
                        'range': parse_range(line[1]),
                        'prob': line[2],
                    }, ignore_index=True)
            return data_adapt

        # Initialization.
        self.data = pd.DataFrame()
        if data_ext is None:
            print(dataDir)
            self.data_ext = parse_adaptive(dataDir)
        else:
            self.data_ext = data_ext

        if os.path.exists(Path(storeDir) / 'collected_data.csv'):
            with open(Path(storeDir) / 'collected_data.csv', 'r') as d:
                self.data = pd.read_csv(d)
        else:
            for d in os.listdir(dataDir):
                if d.startswith('host'):
                    data_t = pd.DataFrame(collect_data(
                        Path(dataDir) / str(d) / 'data'))
                    data_t['host'] = d
                    self.data = self.data.append(data_t, ignore_index=True)

            with open(Path(storeDir) / 'collected_data.csv', 'w') as d:
                d.write(self.data.to_csv())

        """
        Postprocess obtained data to work with them further.
        """
        self.runs = pd.unique(self.data['run'])
        self.rngs = pd.unique(self.data['range'])
        self.hosts = pd.unique(self.data['host'])
        self.steps = pd.unique(self.data['step'])
        self.methods = pd.unique(self.data['method'])

        self.__timeInfo = False
        self.__probInfo = False
        self.__spInfo = False

        self.data_rt = pd.DataFrame({
            'host': [],
            'range': [],
            'step': [],
            'method': [],
        })

        for h in self.hosts:
            for r in self.rngs:
                for m in self.methods:
                    for s in self.steps:
                        self.data_rt.loc[len(self.data_rt.index)] = [
                            h, r, s, m]

    # internal interface.
    def __time_info(self):
        self.data_rt.insert(0, 'mean_time', 0)
        self.data_rt.insert(0, 'std_time', 0)

        for h in self.hosts:
            for r in self.rngs:
                for m in self.methods:
                    for s in self.steps:

                        sel = (self.data['host'] == h) & (
                            self.data['range'] == r) & (
                            self.data['method'] == m) & (
                            self.data['step'] == s)
                        sel_rt = (self.data_rt['host'] == h) & (
                            self.data_rt['range'] == r) & (
                            self.data_rt['method'] == m) & (
                            self.data_rt['step'] == s)

                        mt = self.data[sel]['time'].to_numpy()

                        self.data_rt.loc[sel_rt,
                                         'mean_time'] = float(mt.mean())
                        self.data_rt.loc[sel_rt, 'std_time'] = float(mt.std())

        # filling the 'rt' column
        self.data_rt.insert(0, 'rt', 0)
        self.data_rt.insert(0, 'rstd_time', 0)

        for h in self.hosts:
            for r in self.rngs:
                sel = (self.data_rt['host'] == h) & (
                    self.data_rt['range'] == r)
                max_time = self.data_rt[sel]['mean_time'].max()
                self.data_rt.loc[sel,
                                 'rt'] = self.data_rt[sel]['mean_time'] / max_time

        # filling the 'frt' column
        self.data_rt.insert(0, 'frt', 0)
        for r in self.rngs:
            for s in self.steps:
                for m in self.methods:
                    sel = (self.data_rt['range'] == r) & (
                        self.data_rt['step'] == s) & (
                        self.data_rt['method'] == m)

                    mid = self.data_rt[sel]['rt'].to_numpy().mean()
                    self.data_rt.loc[sel, 'frt'] = (
                        self.data_rt[sel]['rt'] - mid) / mid

        print(self.data_rt)

    # public interface
    def time_info(self) -> pd.DataFrame:
        if not self.__timeInfo:
            self.__timeInfo = True
            self.__time_info()

        return self.data_rt

    # internal interface
    def __prob_info(self):

        # filling the 're' column, 6 formula
        self.data_rt.insert(0, 'prob', 0)
        self.data_rt.insert(0, 're', 0)
        for r in self.rngs:
            sel = (self.data['range'] == r) & (
                self.data['step'] == REF_STEP) & (self.data['method'] == REF_METHOD)
            base_prob = self.data[sel]['prob'].to_numpy().mean()

            for m in self.methods:
                for s in self.steps:
                    sel = (self.data['range'] == r) & (
                        self.data['method'] == m) & (self.data['step'] == s)
                    sel_t = (self.data_rt['range'] == r) & (
                        self.data_rt['method'] == m) & (self.data_rt['step'] == s)

                    prob = self.data[sel]['prob'].to_numpy().mean()
                    self.data_rt.loc[sel_t, 'prob'] = prob
                    self.data_rt.loc[sel_t, 're'] = (
                        prob - base_prob) / base_prob

        # 8 formula
        if self.data_ext is not None:
            self.data_rt.insert(0, 'ext_prob', 0)
            for r in self.rngs:
                print(self.data_ext)
                sel_ext = (self.data_ext['range'] == r)
                ext_prob = float(self.data_ext[sel_ext]['prob'].to_numpy()[0])
                for m in self.methods:
                    for s in self.steps:
                        sel = (self.data['range'] == r) & (
                            self.data['method'] == m) & (self.data['step'] == s)
                        sel_t = (self.data_rt['range'] == r) & (
                            self.data_rt['method'] == m) & (self.data_rt['step'] == s)

                        prob = self.data[sel]['prob'].to_numpy().mean()
                        # self.data_rt.loc[sel_t, 'prob'] = prob
                        self.data_rt.loc[sel_t, 'ext_prob'] = (
                            prob - ext_prob) / ext_prob

        # filling the 'fre' column

        # self.data_rt.insert(0, 'fre', 0)
        # for r in self.rngs:
        #     for s in self.steps:
        #         for m in self.methods:
        #             sel = (self.data_rt['range'] == r) & (
        #                 self.data_rt['step'] == s) & (self.data_rt['method'] == m)
        #             mid = self.data_rt[sel]['re'].to_numpy().mean()
        #             self.data_rt.loc[sel, 'fre'] = (
        #                 self.data_rt[sel]['re'] - mid) / mid

        print(self.data_rt)

    # public interface
    def prob_info(self) -> pd.DataFrame:
        if not self.__probInfo:
            self.__probInfo = True
            self.__prob_info()

        return self.data_rt

    # internal interface
    def __sp_info(self):  # also survival probability
        self.data_rt.insert(0, 'sp', 0)
        for r in self.rngs:
            for s in self.steps:
                for m in self.methods:
                    sel = (self.data_rt['range'] == r) & (
                        self.data_rt['step'] == s) & (self.data_rt['method'] == m)
                    self.data_rt.loc[sel, 'sp'] = self.data_rt[sel]['prob'].to_numpy(
                    ).mean()

        print(self.data_rt)

    # public interface
    def sp_info(self) -> pd.DataFrame:
        if not self.__spInfo:
            self.__spInfo = True
            self.__sp_info()

        return self.data_rt

    def all_info(self) -> pd.DataFrame:
        # rely on side effect of calling methods.
        self.time_info()
        self.prob_info()
        self.sp_info()

        return self.data_rt


def gen_graf(data, types, methods=None, steps=None, hosts=None, rngs=None):
    """
    Generate data files from results of program run.

    """

    wdat = data.all_info()

    if steps is None:
        steps = pd.unique(wdat['step'])
    if rngs is None:
        rngs = pd.unique(wdat['range'])
    if hosts is None:
        hosts = pd.unique(wdat['host'])
    if methods is None:
        methods = pd.unique(wdat['method'])

    ret_data = pd.DataFrame()
    ret_data.insert(0, 'step', 0)
    ret_data.insert(1, 'range', 0)

    for r in rngs:
        ret_data = ret_data.append(pd.DataFrame(
            {'step': steps, 'range': r}), ignore_index=True)

    index = 2
    for h in hosts:
        for m in methods:
            for t in types:
                cname = f'{m}_{h}_{t}'
                ret_data.insert(index, cname, 0)
                index += 1
                for r in rngs:
                    for s in steps:
                        sel_t = (wdat['host'] == h) & (
                            wdat['method'] == m) & (
                            wdat['range'] == r) & (
                            wdat['step'] == s)
                        sel_ret = (ret_data['range'] == r) & (
                            ret_data['step'] == s)
                        ret_data.loc[sel_ret, cname] = wdat[sel_t][t].to_numpy()[
                            0]  # ???????????????????????

    # удалить
    with open(Path("all_graphs") / 'data.csv', 'w') as d:
        d.write(wdat.to_csv())
    return ret_data
