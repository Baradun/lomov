import json
import os


def info(file_text):
    text_list = file_text.split()
    # method = text[list.index('start') + 2]
    start = text_list[text_list.index('start') + 2]
    end = text_list[text_list.index('end') + 2]
    step = text_list[text_list.index('step') + 2]
    time = text_list[text_list.index('time') + 2]
    P = text_list[text_list.index('P') + 2]

    return start, end, step, time, P


def collect_statistics(folder_name, output_file_name):
    list_files = os.listdir(folder_name)
    with open(output_file_name, 'w') as output_file:
        for file in list_files:

            if file.startswith('Cf4_3'):
                method = 'Cf4_3'
            elif file.startswith('Cf4'):
                method = 'Cf4'
            else:
                method = file[0:2]

            with open(f'{folder_name}/{file}', 'r') as f:
                data = f.read()
                start, end, step, time, _ = info(data)
                output_file.write(f'{method} {start} {end} {step} {time}\n')


def data_to_graf(folder_name):
    data_list = []
    list_files = os.listdir(folder_name)

    for log_file in list_files:

        if log_file.startswith('Cf4_3'):
            method = 'Cf4_3'
        elif log_file.startswith('Cf4'):
            method = 'Cf4'
        else:
            method = log_file[0:2]

        with open(f'{folder_name}/{log_file}', 'r') as f:
            data = f.read()
            start, end, step, time, P = info(data)
            data_list.append({
                'method': method,
                'start': start,
                'end': end,
                'step': step,
                'time': time,
                'P': P,
            })
    return data_list


def make_graf_file(data, start, end, method):
    for i in data:
        if (str(start) == i.get('start') and
            str(end) == i.get('end') and
            method == i.get('method') and
            '1e-10' == i.get('step')):

            basis = i
            print(basis)
            break
    
    for method_name in ['M2', 'M4', 'M6', 'Cf4', 'Cf4_3']:
        with open(f'for_gnuplot_{method_name}.dat', 'w') as output_file:
            for i in data:
                if (str(start) == i.get('start') and
                    str(end) == i.get('end') and
                    method_name == i.get('method')):

                    err = abs(float(i.get('P')) - float(basis.get('P'))) / float(basis.get('P'))
                    step = i.get('step')
                    P = i.get('P')
                    output_file.write(f'{step} {err} {P}\n')


if __name__ == '__main__':
    # log_files_dir = 'logs_0.1_0.15'
    # output_file = '0.1_0.15.txt'
    # collect_statistics(log_files_dir, output_file)

    # log_files_dir = 'logs_0.1_0.2'
    # output_file = '0.1_0.2.txt'
    # collect_statistics(log_files_dir, output_file)

    # log_files_dir = 'logs_0.1_0.25'
    # output_file = '0.1_0.25.txt'
    # collect_statistics(log_files_dir, output_file)

    
    # log_files_dir = 'logs/logs_0.1_0.15'    
    # data.append(data_to_graf(log_files_dir))

    log_files_dir = 'logs/logs_0.1_0.2'
    data = (data_to_graf(log_files_dir))

    # log_files_dir = 'logs/logs_0.1_0.25'
    # data.append(data_to_graf(log_files_dir)[0])
    #print(data)

    make_graf_file(data, 0.1, 0.2, 'M4')
