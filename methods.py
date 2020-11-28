import numpy as np
import subprocess
from math import sqrt, sin
from exponentiation.exp import matrix_exp_leja as exp
import numpy.linalg as la
import os as os


class WrongNumberOfPoints(Exception):
    pass


def str_to_list(string):
    list_str = string.split('\n')
    N = int(list_str[0])
    list_str = list_str[1]
    list_str = list_str.replace('[', ' ')
    list_str = list_str.replace(']', ' ')
    l = []
    for i in list_str.split(','):
        l.append(float(i))
    if N == len(l):
        return l
    else:
        return WrongNumberOfPoints


def run_file_and_read(calc_file, read_file):
    base_dir = 'julia-fn/'
    subprocess.run(['julia', base_dir+calc_file])
    result = subprocess.run(['julia', base_dir+read_file], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    try:
        return str_to_list(result)
    except WrongNumberOfPoints as e:
        return e


try:
    leja_points = np.array(run_file_and_read('gen-lp.jl', 'read-lp.jl'))
    div_diff = np.array(run_file_and_read('divd-diff-calc.jl', 'read-dde.jl'))
except WrongNumberOfPoints:
    print('Something went wrong =(')


a = 123
H0 = np.array([
    [0., 0.],
    [0., a]])

c = sqrt(1-sin(0.437)**2)
W = np.array([
    [c, 1.],
    [1., c]])
v0 = 935.367
n = 10.3

step = 0.01
section = np.arange(0, 1+step, step)


def get_v(t):
    return v0*np.exp(-1*n*t)


print(leja_points[0:5])
print(div_diff[0:5])

Y = np.array([1., 0.])
i = 0
A = H0 + (get_v(i + step / 2.) * W)
omega = step * A * 1j
Y = exp(omega, leja_points, div_diff, 5, Y)
print(f'[{i}] A ', A)
print(f'[{i}] Y ', Y)






for i in section:
    A = H0 + (get_v(i+step/2.) * W)
    omega = step*A*1j
    Y = exp(omega, leja_points, div_diff, 10, Y)
    print(f'[{i}] A ', A)
    print(f'[{i}] Y ', Y)
print(Y, '    ', la.norm(Y))

