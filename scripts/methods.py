#!/usr/bin/env python

import json
import os
from multiprocessing import Pool
from pathlib import Path
import subprocess
import time

BASE_DIR = os.getenv('BASE_DIR', 'main')
RUN_FILE = os.getenv('RUN_FILE', "main")
RUNS = int(os.getenv('RUNS', 10))
CORES = os.getenv('CORES', 12)
SCRIPT_DIR = os.getenv('MESON_SOURCE_ROOT', '.')
WDIR = os.getenv('MESON_BUILD_ROOT', '.')


def run_subprocess(params):
    """Run a program with given parameters.

    """
    # params = (start, stop, step, method, output_file)
    command = './' + BASE_DIR + '/' + RUN_FILE + ' ' + params[0] + \
        ' ' + params[1] + ' ' + params[2] + ' ' + \
        params[3] + ' > ' + params[4] + ' 2>&1'

    try:
        result = subprocess.run([command], shell=True, check=True)
        if result.returncode == 0:
            return 0
        return RuntimeError
    except subprocess.SubprocessError as exeption:
        return exeption


def get_params(params_file, log_dir):
    """Set up parameters to run a program.

    """

    list_params = []

    data = 0
    with open(params_file, 'r') as file:
        data = file.read()
    data_json = json.loads(data)

    # There json file structure is unclear.
    for method_data in data_json.get('methods'):
        method_name = method_data.get('method')
        start = str(method_data.get('start'))
        stop = str(method_data.get('stop'))
        step = str(method_data.get('step'))
        log_file_name = Path(log_dir / method_name)

        for j in range(RUNS):
            list_params.append((
                start,
                stop,
                step,
                method_name,
                log_file_name / f'run_{j}.log'
            ))

    return list_params


def run(log_dir, json_file):
    """Prepare all necessary to run programs in parallel.

    """
    list_params = get_params(json_file, log_dir)
    process_pool = Pool(CORES)
    result = process_pool.map(run_subprocess, list_params)
    print(result)
    
    
    process_pool.close()
    process_pool.join()


if __name__ == '__main__':
    """Main 'module' of the script.

    """

    logs_dir = Path("logs")
    if not os.path.isdir(logs_dir):
        os.mkdir(logs_dir)

    json_dir = Path("methods")
    if not os.path.isdir(json_dir):
        print(f"Can't work without '{json_dir}' directory with json files!")
        exit(1)

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
    log_dir = logs_dir / "01_03"
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    json_file = json_dir / "01_03.json"
    if not os.path.isfile(json_file):
        print(f"Can't run this cycle, we need a '{json_file}' in '{json_dir}'!")
        exit(2)
    par_list = get_params(json_file, log_dir);
    print(f"get_params returned: {par_list}")
    # run(log_dir, json_file)

    print("end prgrm")
    print(time.time() - start_time)
