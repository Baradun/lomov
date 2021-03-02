#!/usr/bin/env python

import json
import os
from multiprocessing import Pool
import subprocess
import time

BASE_DIR = os.getenv('BASE_DIR', 'main')
RUN_FILE = os.getenv('RUN_FILE', "main")
RUNS = os.getenv('RUNS', 10)
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

    for method_data in data_json[0].get('methods'):
        method_name = method_data.get('method')
        start = str(method_data.get('start'))
        stop = str(method_data.get('stop'))
        step = str(method_data.get('step'))
        log_file_name = (log_dir + method_name +
                         '_' + start + '_' + stop + '_' + step + '.log')

        for j in range(RUNS):
            list_params.append((
                start,
                stop,
                step,
                method_name,
                log_file_name.replace(".log", f'_{j}.log'),
            ))

    return list_params


def run():
    """Prepare all necessary to run programs in parallel.

    """
    list_params = get_params()
    process_pool = Pool(CORES)
    result = process_pool.map(run_subprocess, list_params)
    print(result)


    process_pool.close()
    process_pool.join()


if __name__ == '__main__':
    """Main 'module' of the script.

    """

    ### We need to prepare some directories.
    ### LOG_FILE_DIR must exist before all below to be run.

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
    run("logs_0.1_0.3/", "methods_0.1_0.3.json")

    print("end prgrm")
    print(time.time() - start_time)
