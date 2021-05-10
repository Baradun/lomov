#!/usr/bin/python3

import os
import pathlib
import sys
from pathlib import Path
from pprint import pprint

DATA_DIR = os.getenv("DATA_DIR", "data/")
FILE_MANE = ['gt0', 'gt1', 'gt2']
METHODS = ["M2", "M4", "M6", "CF4", "CF4:3"]


def gt2():
    steps = []
    strtwh = 'gt2'
    data = {}
    for i in METHODS:
        data[i] = []

    for i in dirs:
        for f in os.listdir(i + '/graphs'):
            if f.startswith(strtwh):
                with open(i+'/graphs/' + f, 'r') as file:
                    file.readline()
                    file.readline()
                    line = file.readline()
                    while (line != ''):
                        prms = line.split('\t')
                        step = prms[0]
                        if step not in steps:
                            steps.append(step)

                        index = 1
                        for mth in METHODS:
                            data[mth].append(
                                {
                                    'step': step,
                                    'value': prms[index],
                                    'host': i,
                                }
                            )
                            index += 1

                        line = file.readline()

    print("# step(1)", end=' ')
    start = 1
    end = len(dirs)
    for i in METHODS:
        print(f'{i}({start+1}-{end+2})', end=' ')
        start += len(dirs) + 1
        end += len(dirs) + 1 
    print()

    for s in steps:
        print(s, end=' ')
        for k in data.keys():
            count = 0
            summa = 0
            for i in data[k]:
                if float(s) == float(i.get('step')):
                    count += 1
                    summa += float(i.get('value'))
            print(f'{summa/count}', end=' ')

            for host in dirs:
                count = 0
                summa = 0
                for i in data[k]:
                    if i.get('host') == host and i.get('step') == s:
                        summa += float(i.get('value'))
                        count += 1.0
                print(f'{summa/count}', end=' ')
        print()
    print('\n\n')
    for i, d in enumerate(dirs):
        print(f'# {i+1} ', d[d.index('host'):])


def gt1():
    strtwh = 'gt1'
    data = {
        'M2': [],
        "M4": [],
        "M6": [],
        "CF4": [],
        "CF4:3": [],
    }

    for i in dirs:
        for f in os.listdir('./'+i + '/graphs'):
            if f.startswith(strtwh):
                with open('./'+i+'/graphs/' + f, 'r') as file:
                    file.readline()
                    file.readline()
                    line = file.readline()
                    while (line != ''):
                        prms = line.split('\t')
                        step = prms[0]
                        if step not in steps:
                            steps.append(step)
                        index = 1
                        for mth in METHODS:
                            data[mth].append(
                                {
                                    'step': step,
                                    'value': prms[index],
                                }
                            )
                            index += 1

                        line = file.readline()

    for s in steps:
        print(s, end=' ')
        for k in data.keys():
            count = 0
            summa = 0
            for i in data[k]:
                if float(s) == float(i.get('step')):
                    count += 1
                    summa += float(i.get('value'))
            print(f'{summa/count}', end=' ')
        print()


def gt0():
    steps = []
    strtwh = 'gt0'
    data = {}
    for i in METHODS:
        data[i] = []

    for i in dirs:
        for f in os.listdir(i + '/graphs'):
            if f.startswith(strtwh):
                with open(i+'/graphs/' + f, 'r') as file:
                    file.readline()
                    file.readline()
                    line = file.readline()
                    while (line != ''):
                        prms = line.split('\t')
                        step = prms[0]
                        
                        if step not in steps:
                            steps.append(step)

                        index = 1
                        for mth in METHODS:
                            data[mth].append(
                                {
                                    'step': step,
                                    'error': prms[index],
                                    'SP': prms[index+1],
                                    'host': i,
                                }
                            )
                            index += 2
                        line = file.readline()

    for s in steps:
        print(s, end=' ')
        for k in data.keys():
            count = 0
            error = 0
            SP = 0
            for i in data[k]:
                if float(s) == float(i.get('step')):
                    count += 1
                    error += float(i.get('error'))
                    SP += float(i.get('SP'))
            print(f'{error/count} {SP/count}', end=' ')
            
            for host in dirs:
                count = 0
                error = 0
                SP = 0
                for i in data[k]:
                    if i.get('host') == host and i.get('step') == s:
                        error += float(i.get('error'))
                        SP += float(i.get('SP'))
                        count += 1.0
                print(f'{error/count} {SP/count}', end=' ')
        print()
    print('\n\n')
    for i, d in enumerate(dirs):
        print(f'# {i+1} ', d[d.index('host'):])

# Не работает
def gt_unvrsl(strtwh):
    dirs = []
    steps = []

    data = {}
    for i in METHODS:
        data[i] = []

    for i in dirs:
        for f in os.listdir('./'+i + '/graphs'):
            if f.startswith(strtwh):
                with open('./'+i+'/graphs/' + f, 'r') as file:
                    file.readline()
                    file.readline()
                    line = file.readline()
                    while (line != ''):
                        prms = line.split('\t')
                        step = prms[0]
                        prms_numb = (len(prms) - 1)/len(METHODS)

                        if step not in steps:
                            steps.append(step)

                        index = 1
                        for mth in METHODS:

                            data[mth].append(
                                {
                                    'step': step,
                                    'value': prms[index],
                                }
                            )
                            index += 1

                        line = file.readline()
# gt_unvrsl('gt0')


if __name__ == '__main__':
    graf_type = 0
    if len(sys.argv) == 2:
        graf_type = sys.argv[1]
    if len(sys.argv) == 3:
        graf_type = sys.argv[1]
        DATA_DIR = sys.argv[2]

    dirs = []
    for i in os.listdir(DATA_DIR):
        if i.startswith('host'):
            dirs.append(DATA_DIR + i)

    if graf_type == '0':
        gt0()
    if graf_type == '1':
        gt1()
    if graf_type == '2':
        gt2()
