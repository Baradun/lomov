import json
import multiprocessing
import os
import subprocess
import time 

base_dir = 'main/'
run_file = 'main'
log_files_dir = 'logs/'
runs = 10


def run(run_file, start, stop, step, method, output_file):
    command = './' + base_dir + '/' + run_file + ' ' + start + \
        ' ' + stop + ' ' + step + ' ' + method + ' > ' + output_file
    try:
        # result = subprocess.run(['julia', base_dir+read_file], stdout=subprocess.PIPE)
        # result = result.stdout.decode('utf-8')
        result = subprocess.run([command], shell=True, stdout=str)

        if result.returncode == 0:
            return 0
        else:
            return RuntimeError
    except subprocess.SubprocessError as e:
        return e


if __name__ == '__main__':
    
    data = 0
    with open('methods.json', 'r') as f:
        data = f.read()
    data_json = json.loads(data)
    #multiprocessing.Process(run, args=[])
    
    list_process = []
    
    start_time = time.time()
    print('start')

    for i, method_data in enumerate(data_json[0].get('methods')):
        method_name = method_data.get('method')
        start = str(method_data.get('start'))
        stop = str(method_data.get('stop'))
        step = str(method_data.get('step'))
        log_file_name = (log_files_dir + method_name + 
            '_' + start + '_' + stop + '_' + step + '.log')
        
        start_time_runs = time.time()
        for _ in range(runs):
            run(run_file, start, stop, step, method_name, log_file_name)
        
        print(i ,'\t', log_file_name, '\tt:',(time.time() - start_time_runs)/runs)


    print("end")
    print(time.time() - start_time)


# TODO: дописать ввывод в файл 