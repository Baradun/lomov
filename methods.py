import json
from multiprocessing import Pool
import subprocess
import time

BASE_DIR = 'main/'
RUN_FILE = 'main'
RUNS = 10
CORES = 12


def run_subprocess(params):
    """"

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


def get_params():
    """

    """

    list_params = []

    data = 0
    with open(PARAMS_FILE, 'r') as file:
        data = file.read()
    data_json = json.loads(data)

    for method_data in data_json[0].get('methods'):
        method_name = method_data.get('method')
        start = str(method_data.get('start'))
        stop = str(method_data.get('stop'))
        step = str(method_data.get('step'))
        log_file_name = (LOG_FILE_DIR + method_name +
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
    """

    """
    list_params = get_params()
    process_pool = Pool(CORES)
    result = process_pool.map(run_subprocess, list_params)
    print(result)
    
    
    process_pool.close()
    process_pool.join()


if __name__ == '__main__':

    start_time = time.time()
    print('start prgrm')

    # LOG_FILE_DIR = 'logs/logs_0.1_0.15/'
    # PARAMS_FILE = 'logs/methods_0.1_0.15.json'
    # run()

    # print('#'*80)
    # print('time = ', time.time() - start_time)
    # print('#'*80)

    # LOG_FILE_DIR = 'logs/logs_0.1_0.2/'
    # PARAMS_FILE = 'logs/methods_0.1_0.2.json'
    # run()

    # print('#'*80)
    # print('time = ', time.time() - start_time)
    # print('#'*80)

    LOG_FILE_DIR = 'logs_0.1_0.3/'
    PARAMS_FILE = 'methods_0.1_0.3.json'
    run()

    print("end prgrm")
    print(time.time() - start_time)
