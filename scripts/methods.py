#!/usr/bin/env python

import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path
import subprocess
import time

BASE_DIR = os.getenv('BASE_DIR', 'main')
RUN_FILE = os.getenv('RUN_FILE', "main")
RUNS = int(os.getenv('RUNS', '10'))
CORES = int(os.getenv('CORES', '12'))
DATA_DIR = os.getenv('DATA_DIR', 'data')
JSON_DIR = os.getenv('JSON_DIR', 'methods')
JSON_WORK = os.getenv('JSON_WORK', 'work.json')
SCRIPT_DIR = os.getenv('MESON_SOURCE_ROOT', '.')
WDIR = os.getenv('MESON_BUILD_ROOT', '.')


def run_subprocess(params):
    """Run a program with given parameters.

    """
    # params = (start, stop, step, method, output_file)
    command = [ str(params["program"]), params["start"], params["end"],
            params["step"], params["method"] ]

    try:
        result = subprocess.run(command, capture_output=True, check=True,
                text=True)
        with open(params["dat_file"], "w") as f:
            f.write(result.stdout)
        if result.returncode == 0:
            return 0
        return RuntimeError
    except subprocess.SubprocessError as exeption:
        return exeption


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
            dat_file_p = f"{method_name}_{start},{stop}_{step}_r{j}.dat"
            dat_file = Path(data_dir / dat_file_p)
            list_params.append({
                "program" : exe,
                "start" : start,
                "end" : stop,
                "step" : step,
                "method" : method_name,
                "dat_file" : dat_file
            })

    return list_params


def run(data_dir, json_file):
    """Prepare all necessary to run programs in parallel.

    """
    list_params = get_params(json_file, data_dir)
    process_pool = Pool(CORES)
    result = process_pool.map(run_subprocess, list_params)
    print(result)

    process_pool.close()
    process_pool.join()


if __name__ == '__main__':

    data_dir = Path(DATA_DIR)
    if not os.path.isdir(data_dir):
        try:
            os.mkdir(data_dir)
        except FileExistsError as err:
            print(f"We need directory '{DATA_DIR}' to save generated data but \
                    we got error while trying to create one: {err}")
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

    json_dir = Path(JSON_DIR)
    if not os.path.isdir(json_dir):
        print(f"We expect that JSON file with work load should be in \
                '{JSON_DIR}' directory but that one doesn't exist or is not a \
                directory!")
        sys.exit(1)

    start_time = time.time()
    print('start prgrm')

    # LOG_FILE_DIR = 'logs/logs_0.1_0.15/'
    # PARAMS_FILE = 'logs/methods_0.1_0.15.json'
    # run('logs/logs_0.1_0.15/', 'logs/methods_0.1_0.15.json')

    # print('#'*80)
    # print('time = ', time.time() - start_time)
    # print('#'*80)

    # LOG_FILE_DIR = 'logs/logs_0.1_0.2/'
    # PARAMS_FILE = 'logs/methods_0.1_0.2.json'
    # run('logs/logs_0.1_0.2/', 'logs/methods_0.1_0.2.json')

    # print('#'*80)
    # print('time = ', time.time() - start_time)
    # print('#'*80)

    #  LOG_FILE_DIR = 'logs_0.1_0.3/'
    #  PARAMS_FILE = 'methods_0.1_0.3.json'
    json_file = json_dir / JSON_WORK
    if not os.path.isfile(json_file):
        print(f"Can't do anything, we need a '{JSON_WORK}' in '{JSON_DIR}'!")
        sys.exit(2)
    run(data_dir, json_file)

    print("end prgrm")
    print(time.time() - start_time)
