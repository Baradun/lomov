#!/usr/bin/env python

import json
import os
from pathlib import Path

DATA_DIR = os.getenv("METHODS_DATA_DIR", "data")
OUT_DIR = os.getenv("METHODS_GRAPH_DIR", "graphs")
METHODS = [ "M2", "M4", "M6", "CF4", "CF4:3" ]
MAX_STEP = '1e-10'

def info(content):
    """Extract and return a list of necessary parameters from a file content.
    """

    text_list = content.split()
    # method = text[list.index('start') + 2]
    start = text_list[text_list.index('start') + 2]
    end = text_list[text_list.index('end') + 2]
    step = text_list[text_list.index('step') + 2]
    time = text_list[text_list.index('time') + 2]
    P = text_list[text_list.index('P') + 2]

    return start, end, step, time, P


def collect_statistics(folder_name, output_file_name):
    """Write data to a file being plotted by gnuplot.
    """

    list_files = os.listdir(folder_name)
    with open(output_file_name, 'w') as output_file:
        for file in list_files:

            if file.startswith(METHODS[4]):
                method = METHODS[4]
            elif file.startswith(METHODS[3]):
                method = METHODS[3]
            else:
                method = file[0:2]

            with open(f'{folder_name}/{file}', 'r') as f:
                data = f.read()
                start, end, step, time, _ = info(data)
                output_file.write(f'{method} {start} {end} {step} {time}\n')


def get_data():
    """Get data from a file for gnuplot plotting.
    """

    data_list = []
    list_files = os.listdir(DATA_DIR)

    for dat_file in list_files:

        if dat_file.startswith(METHODS[4]):
            method = METHODS[4]
        elif dat_file.startswith(METHODS[3]):
            method = METHODS[3]
        else:
            method = dat_file[0:2]

        with open(Path(DATA_DIR)/dat_file, 'r') as f:
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


def make_gp_dat(data, start, end, method, graf_type=0):
    """Make data files to be plotted by gnuplot.

    Prefix data files with graph type.
    """

    # x = steps; y = err
    if graf_type == 0:
        for i in data:
            if (str(start)   == i['start']  and
                str(end)     == i['end']    and
                method       == i['method'] and
                MAX_STEP     == i['step']   ):

                basis = i
                #  print(basis)
                break

        for method_name in METHODS:
            with open(Path(OUT_DIR)/f'gt0_{method_name}.dat', 'w') as gp_dat:
                gp_dat.write(f"## STEP\tRELATIVE ERROR\tSURVIVAL PROBABILITY\n")
                for i in data:
                    if (str(start)   == i['start'] and
                        str(end)     == i['end']   and
                         method_name == i['method']):

                        err = abs(float(i['P']) -
                                  float(basis['P'])) / float(basis['P'])
                        step = i['step']
                        P = i['P']
                        gp_dat.write(f'{step} {err} {P}\n')

        #  with open(Path(OUT_DIR)/"gt0.dat", "w") as gp_dat:
        #      gp_dat.write(f"## STEP\tREL_ERR(M2)\tREL_ERR(M4)\t\
        #              REL_ERR(M6)\tREL_ERR(CF4)\tREL_ERR(CF4:3)\t\
        #              SUR_PROB(M2)\tSUR_PROB(M4)\tSUR_PROB(M6)\t\
        #              SUR_PROB(CF4)\tSUR_PROB(CF4:3)\n")
        #      for i in data:
        #          step = i['step']
        #          m2   = i['M2']
        #          m4   = i['M4']
        #          m6   = i['M6']
        #          cf4  = i['CF4']
        #          cf43 = i['CF4:3']
        #          gp_dat.write(f"{step}\t{m2}\t{m4}\t{m6}\t{cf4}\t{cf43}\n")

    # x = step; y = time
    if graf_type == 1:
        for method_name in METHODS:
            with open(Path(OUT_DIR)/f'gt1_{method_name}.dat', 'w') as gp_dat:
                gp_dat.write(f"## STEP\tEXECUTION TIME\n")
                for i in data:
                    if (str(start)  == i['start'] and
                        str(end)    == i['end']   and
                        method_name == i['method']):
                        
                        step = i['step']
                        time = i['time']
                        gp_dat.write(f'{step} {time}\n')

        with open(Path(OUT_DIR)/"gt1.dat", "w") as gp_dat:
            gp_dat.write(f"## STEP\tEXEC TIME(M2)\tEXEC TIME(M4)\t\
                    EXEC TIME(M6)\tEXEC TIME(CF4)\tEXEC TIME(CF4:3)\n")
            for i in data:
                step = i['step']
                time = i['time']
                m2   = i['M2']
                m4   = i['M4']
                m6   = i['M6']
                cf4  = i['CF4']
                cf43 = i['CF4:3']
                gp_dat.write(f"{step}\t{m2}\t{m4}\t{m6}\t{cf4}\t{cf43}\n")

    
    # x = step; y = time
    if graf_type == 2:
        max_time = float(data[0]['time'])
        for i in data:
            if (str(start) == i['start'] and
                str(end)   == i['end']   ):

                time = float(i['time'])
                if time > max_time:
                    max_time = time


        for method_name in METHODS:
            with open(Path(OUT_DIR)/f'gt2_{method_name}.dat', 'w') as gp_dat:
                gp_dat.write(f"## STEP\tRELATIVE EXECUTION TIME (to M6 1e-10)\n")
                for i in data:
                    if (str(start)  == i['start'] and
                        str(end)    == i['end']   and
                        method_name == i['method']):

                        step = i['step']
                        time = float(i['time']) / max_time
                        gp_dat.write(f'{step} {time}\n')


if __name__ == '__main__':
    """Main 'module' of the script.
    """

    if not os.path.isdir(Path(DATA_DIR)):
        print(f"We expect data to be in '{DATA_DIR}' directory, but it missing!")
        sys.exit(1)

    if not os.path.isdir(Path(OUT_DIR)):
        try:
            os.mkdir(Path(OUT_DIR))
        except FileExistsError as err:
            print(f"We need directory '{OUT_DIR}' to store generated file but \
                    we got error while trying to create one: {err}")
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

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

    # Do we need () around?
    data = (get_data())

    # log_files_dir = 'logs/logs_0.1_0.25'
    # data.append(data_to_graf(log_files_dir)[0])
    # print(data)

    h_m = "M6"
    start = 0.1
    end = 0.2
    make_gp_dat(data, start, end, h_m, 0)
    make_gp_dat(data, start, end, h_m, 1)
    make_gp_dat(data, start, end, h_m, 2)
