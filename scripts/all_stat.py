import os
from pathlib import Path
import pathlib
import sys
from pprint import pprint

DATA_DIR = os.getenv("METHODS_DATA_DIR", "data/")
FILE_MANE = ['gt0', 'gt1', 'gt2']
METHODS = ["M2", "M4", "M6", "CF4", "CF4:3"]
dirs = []
steps = []

for i in os.listdir(DATA_DIR):
    if i.startswith('host'):
        dirs.append(DATA_DIR + i)


def gt2():
    strtwh = 'gt2'
    data = {}
    for i in METHODS:
        data[i] = []


    for i in dirs:
        for f in os.listdir(i + '/graphs'):
            if f.startswith(strtwh):
                with open(i+'/graphs/'+ f, 'r') as file:
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
                            index +=1
                        
                        line = file.readline()
        # print(i)
        # for s in steps:
        #     print(s, end=' ')
        #     for k in data.keys():
        #         count = 0
        #         summa = 0
        #         for i in data[k]:
        #             if float(s) == float(i.get('step')):
        #                 count += 1
        #                 summa += float(i.get('value'))
        #         print(f'{summa/count}', end=' ')
        #     print()

    
    print('step M2(2-11) M4(12-21) M6(22-31) CF4(32-41) CF4:3(42-51)')
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
def gt1():
    strtwh = 'gt1'
    data = {
        'M2': [],
        "M4":[],
        "M6":[],
        "CF4":[],
        "CF4:3":[],
    }


    for i in dirs:
        for f in os.listdir('./'+i + '/graphs'):
            if f.startswith(strtwh):
                with open('./'+i+'/graphs/'+ f, 'r') as file:
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
                                    'step':step,
                                    'value': prms[index],
                                }
                            )
                            index +=1
                        
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
    strtwh = 'gt0'
    data = {}
    for i in METHODS:
        data[i] = []


    for i in dirs:
        for f in os.listdir('./'+i + '/graphs'):
            if f.startswith(strtwh):
                with open('./'+i+'/graphs/'+ f, 'r') as file:
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
                                    'step':step,
                                    'error': prms[index],
                                    'SP':prms[index+1]
                                }
                            )
                            index +=2
                        
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
        print()



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
                with open('./'+i+'/graphs/'+ f, 'r') as file:
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
                                    'step':step,
                                    'value': prms[index],
                                }
                            )
                            index +=1
                        
                        line = file.readline()
#gt_unvrsl('gt0')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        graf_type = sys.argv[1]
    if len(sys.argv) == 3:
        graf_type = sys.argv[1]
        DATA_DIR = sys.argv[2]

    if graf_type == '0':
        gt0()
    if graf_type == '1':
        gt1()
    if graf_type == '2':
        gt2()



