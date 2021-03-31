#!/usr/bin/env python3

import curses
import json
import os
import subprocess
import sys
import time
from copy import deepcopy, copy
from multiprocessing import Array, Lock, Pool, Process, process
from pathlib import Path
from subprocess import Popen
from typing import Counter
from random import sample
from pydantic import BaseModel

BASE_DIR = os.getenv('BASE_DIR', 'main')
RUN_FILE = os.getenv('RUN_FILE', 'main')
RUNS = int(os.getenv('RUNS', '10'))
CORES = int(os.getenv('CORES', '12'))
DATA_DIR = os.getenv('DATA_DIR', 'data')
JSON_DIR = os.getenv('JSON_DIR', 'methods')
JSON_WORK = os.getenv('JSON_WORK', 'work.json')
SCRIPT_DIR = os.getenv('MESON_SOURCE_ROOT', '.')
WDIR = os.getenv('MESON_BUILD_ROOT', '.')
METHODS = ['M2', 'M4', 'M6', 'CF4', 'CF4:3']


class Win:
    def __init__(self, list_params):
        self.list_params = copy(list_params)
        self.screen = curses.initscr()
        curses.curs_set(False)
        #curses.start_color()

        self.num_rows, self.num_cols = self.screen.getmaxyx()
        self.win = curses.newwin(self.num_rows, self.num_cols, 0, 0)
        self.win.refresh()

        self.values = self.count()

    def count(self):
        values = []
        for method in METHODS:
            cnt = 0
            for i in self.list_params:
                if method == i.get('method'):
                    cnt += 1
            if cnt > 0:
                values.append({'method': method, 'total': cnt, "finished": 0})
        return values
    
    
    @staticmethod
    def progress(total, finished, colums_number=60):
        
        range = int((colums_number / float(total)) * finished)
        return range*'#' + '.'*int(colums_number - range)

    def update(self, name):
        new_num_rows, new_num_cols = self.screen.getmaxyx()
        if new_num_cols != self.num_cols or new_num_rows != self.num_rows:
            self.num_rows = new_num_rows
            self.num_cols = new_num_cols
            self.win = curses.newwin(self.num_rows, self.num_cols, 0, 0)

        for i in self.values:
            if i.get("method") == name:
                i['finished'] += 1

        line_number = 0
        for deflot in self.values:
            self.win.addstr(line_number, 0, deflot.get('method'))
            total = deflot.get('total')
            finished = deflot.get('finished')

            persent_string = self.progress(total, finished)

            self.win.addstr(
                line_number, 8, f'[{persent_string}] ({finished:>5}/{total:>5})')

            line_number += 1
        # curses.napms(10)
        self.win.refresh()

    def __del__(self):
        curses.endwin()


def run_subprocess(program, start, end, step, method, dat_file):
    """Run a program with given parameters.

    """
    command = [str(program), str(start), str(end), str(step), method]
    # print('sub\t', command)
    with Popen(command, stdout=subprocess.PIPE, text=True) as proc:
        with open(dat_file, 'w') as f:
            f.write(proc.stdout.read())


def get_params(params_file, data_dir):
    """Set up parameters to run a program.

    """

    list_params = []

    data = 0
    with open(params_file, 'r') as file:
        data = file.read()
    data_json = json.loads(data)

    for method_data in data_json.get('work'):
        method_name = method_data.get('method')
        start = str(method_data.get('start'))
        stop = str(method_data.get('stop'))
        step = str(method_data.get('step'))

        exe = Path(BASE_DIR) / Path(RUN_FILE)

        for j in range(RUNS):
            dat_file_p = f'{method_name}_{start},{stop}_{step}_r{j}.dat'
            dat_file = Path(data_dir / dat_file_p)
            list_params.append({
                'program': exe,
                'start': start,
                'end': stop,
                'step': step,
                'method': method_name,
                'dat_file': dat_file
            })

    return sample(list_params, k=len(list_params))


def run(data_dir, json_file):
    """Prepare all necessary to run programs in parallel.

    """
    list_params = get_params(json_file, data_dir)
    run_process = []
    list_process = []
    for i, j in enumerate(list_params):
        program = j.get('program')
        method_name = j.get('method')
        start = j.get('start')
        end = j.get('end')
        step = j.get('step')
        dat_file = j.get('dat_file')
        list_process.append(
            Process(target=run_subprocess, name=j.get('method') , args=(program, start, end, step, method_name, dat_file)))

    # Create window in terminal
    global win
    win = Win(list_params)

    try:
        while len(list_process) != 0:
            if len(run_process) < CORES and len(list_process) != 0:
                run_process.append(list_process.pop(0))
                run_process[len(run_process)-1].start()
                next

            for i in run_process:
                if not i.is_alive():
                    win.update(i.name)
                    run_process.remove(i)

        while len(run_process) != 0:
            for i in run_process:
                if not i.is_alive():
                    win.update(i.name)
                    run_process.remove(i)

    except KeyboardInterrupt as e:
        for i in run_process:
            i.terminate()
    except Exception as e:
        print(e)

    del win


if __name__ == '__main__':

    data_dir = Path(DATA_DIR)
    if not os.path.isdir(data_dir):
        try:
            os.mkdir(data_dir)
        except FileExistsError as err:
            print(f"We need directory '{DATA_DIR}' to save generated data but" +
                  f'we got error while trying to create one: {err}')
        except:
            print('Unexpected error: ', sys.exc_info()[0])
            raise

    json_dir = Path(JSON_DIR)
    if not os.path.isdir(json_dir):
        print('We expect that JSON file with work load should be in '
              f"'{JSON_DIR}' directory but that one doesn't exist or is not a " +
              'directory!')
        sys.exit(1)

    json_file = json_dir / JSON_WORK
    if not os.path.isfile(json_file):
        print(f"Can't do anything, we need a '{JSON_WORK}' in '{JSON_DIR}'!")
        sys.exit(2)

    start_time = time.time()
    print('start prgrm')

    run(data_dir, json_file)

    print('end prgrm')
    print(time.time() - start_time)


# TODO:
# * Change "stop" to "end" in the file "work-do.json"
