#!/usr/bin/env python3

import curses
from copy import Error, deepcopy
import json
import os
import subprocess
import sys
import time
from multiprocessing import Array, Pool, Lock
from pathlib import Path
from subprocess import Popen

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

lock = Lock()


class Win:
    def __init__(self, list_params):
        self.list_params = deepcopy(list_params)
        self.screen = curses.initscr()

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
            values.append({'method': method, 'count': cnt})
        return values

    def count_multi(self):
        values = []
        for method in METHODS:
            cnt = 0
            for i in self.list_params:
                if method == i.get('method') and end_process[win.list_params.index(i)] == 0:
                    cnt += 1
            values.append({'method': method, 'count': cnt})
        return values

    @staticmethod
    def progress(number, totaly, colums_number=60):
        range = int((colums_number / float(totaly)) * number)
        return range*'#' + ' '*int(colums_number - range)

    def update(self):
        new_num_rows, new_num_cols = self.screen.getmaxyx()
        if new_num_cols != self.num_cols or new_num_rows != self.num_rows:
            self.num_rows = new_num_rows
            self.num_cols = new_num_cols
            self.win = curses.newwin(self.num_rows, self.num_cols, 0, 0)

        values = self.count_multi()

        i = 0
        for deflot in self.values:
            for modified in values:
                if deflot.get('method') == modified.get('method'):
                    self.win.addstr(i, 0, deflot.get('method'))
                    total = deflot.get('count')
                    number = modified.get('count')

                    persent_string = self.progress(number, total)

                    self.win.addstr(
                        i, 8, f'[{persent_string}] ({number:>5}/{total:>5})')
                    self.win.refresh()

                    i += 1

    def __del__(self):
        curses.endwin()


def run_subprocess(params):
    """Run a program with given parameters.

    """
    command = [str(params['program']), params['start'], params['end'],
               params['step'], params['method']]

    
    # Terminal info
    end_process[win.list_params.index(params)] = 0
    lock.acquire()
    win.update()
    lock.release()


    with Popen(command, stdout=subprocess.PIPE, text=True) as proc:
        with open(params['dat_file'], 'w') as f:
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

    return list_params


def run(data_dir, json_file):
    """Prepare all necessary to run programs in parallel.

    """
    list_params = get_params(json_file, data_dir)

    # Create window in terminal 
    global win
    global end_process
    end_process = Array('i', len(list_params))
    for i in range(len(list_params)):
        end_process[i] = 1
    win = Win(list_params)


    try:
        process_pool = Pool(CORES)
        result = process_pool.map(run_subprocess, list_params)
        print(result)
    except KeyboardInterrupt as e:
        process_pool.terminate()
    except Error as e:
        print(e)

    process_pool.close()
    process_pool.join()


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
