import json
from multiprocessing import Process
import os
import subprocess
import time

base_dir = 'main/'
run_file = 'main'
log_files_dir = 'logs/'
runs = 2


def run(run_file, start, stop, step, method, output_file):
    command = './' + base_dir + '/' + run_file + ' ' + start + \
        ' ' + stop + ' ' + step + ' ' + method + ' > ' + output_file
    try:
        # result = subprocess.run(['julia', base_dir+read_file], stdout=subprocess.PIPE)
        # result = result.stdout.decode('utf-8')
        result = subprocess.run([command], shell=True)  # stdout=str)

        print(f'end')
        if result.returncode == 0:
            return 0
        else:
            return RuntimeError
    except subprocess.SubprocessError as e:
        return e


def get_list_process():

    list_process = []

    data = 0
    with open('methods.json', 'r') as f:
        data = f.read()
    data_json = json.loads(data)

    for i, method_data in enumerate(data_json[0].get('methods')):
        method_name = method_data.get('method')
        start = str(method_data.get('start'))
        stop = str(method_data.get('stop'))
        step = str(method_data.get('step'))
        log_file_name = (log_files_dir + method_name +
                         '_' + start + '_' + stop + '_' + step + '.log')


        for j in range(runs):
            list_process.append(
                Process(target=run,
                        args=(
                            run_file,
                            start,
                            stop,
                            step,
                            method_name,
                            log_file_name.replace(".log", f'_{j}.log'),
                        )))
            # run(run_file, start, stop, step, method_name, log_file_name)

    print(list_process)
    return list_process


def run_process(cores=4):
    list_process = get_list_process()

    run_process = []
    while len(list_process) != 0:
        if len(run_process) < cores and len(list_process) != 0:
            run_process.append(list_process.pop(0))
            print('добавили', run_process[len(run_process)-1])
            run_process[len(run_process)-1].start()

            next

        for i in run_process:
            if not i.is_alive():
                print("закончил", i)
                run_process.remove(i)

    print(run_process)
    while len(run_process) != 0:
        for i in run_process:
            if not i.is_alive():
                print("финальное закрытие", i)
                run_process.remove(i)


if __name__ == '__main__':
    start_time = time.time()
    print('start')

    run_process()

    print("end prgrm")
    print(time.time() - start_time)


# TODO: название файлов логов
# * - поправить вывод времени в плюсах
