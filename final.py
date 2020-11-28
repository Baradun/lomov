# import subprocess
# from exponentiation.exp import matrix_exp_leja as exp
import numpy as np
#
#
# class WrongNumberOfPoints(Exception):
#     pass
#
#
# def str_to_list(string):
#     list_str = string.split('\n')
#     N = int(list_str[0])
#     list_str = list_str[1]
#     list_str = list_str.replace('[', ' ')
#     list_str = list_str.replace(']', ' ')
#     l = []
#     for i in list_str.split(','):
#         l.append(float(i))
#     if N == len(l):
#         return l
#     else:
#         return WrongNumberOfPoints
#
#
# def run_file_and_read(calc_file, read_file):
#     base_dir = 'julia-fn/'
#     subprocess.run(['julia', base_dir+calc_file])
#     result = subprocess.run(['julia', base_dir+read_file], stdout=subprocess.PIPE)
#     result = result.stdout.decode('utf-8')
#     try:
#         return str_to_list(result)
#     except WrongNumberOfPoints as e:
#         return e
#
#
# try:
#     leja_points = np.array(run_file_and_read('gen-lp.jl', 'read-lp.jl'))
#     div_diff = np.array(run_file_and_read('divd-diff-calc.jl', 'read-dde.jl'))
# except WrongNumberOfPoints:
#     print('Something went wrong =(')
#
# pl = np.array([
#     [1., 0.],
#     [0., -1.]])
#
#
# A1 = np.array([
#     [1., 2.],
#     [0., 1.]])
# A2 = np.array([
#     [1., 4.],
#     [0., -1.]])
# A3 = np.array([
#     [1., -1.],
#     [1., 3.]])
# v1 = np.array([1., 0.])
# v2 = np.array([0., -1.])
# v3 = np.array([1., 2.])
#
#
# # --- First mtrx ---
# delta = exp(A1, leja_points, div_diff, v=v1) -\
#         (np.exp(1.5)*(np.cosh(0.5) + pl*np.sinh(0.5))).dot(v1)
# print('A1 v1: ', delta)
#
#
# delta = exp(A1, leja_points, div_diff, v=v2) -\
#         (np.exp(1.5)*(np.cosh(0.5) + pl*np.sinh(0.5))).dot(v2)
# print('A1 v2: ', delta)
#
#
# delta = exp(A1, leja_points, div_diff, v=v3) -\
#         (np.exp(1.5)*(np.cosh(0.5) + pl*np.sinh(0.5))).dot(v3)
# print('A1 v3: ', delta)
# print('--------------')
#
# # --- Second mtrx ---
# delta = exp(A2, leja_points, div_diff, v=v1) -\
#         (np.cosh(1.0) + A2*np.sinh(1)).dot(v1)
# print('A2 v1: ', delta)
#
# delta = exp(A2, leja_points, div_diff, v=v2) -\
#         (np.cosh(1.0) + A2*np.sinh(1)).dot(v2)
# print('A2 v2: ', delta)
#
# delta = exp(A2, leja_points, div_diff, v=v3) -\
#         (np.cosh(1.0) + A2*np.sinh(1)).dot(v3)
# print('A2 v3: ', delta)
# print('--------------')
#
#
# # --- Third mtrx ---
# delta = exp(A3, leja_points, div_diff, v=v1) -\
#         (A2*np.exp(2.0)).dot(v1)
# print('A3 v1: ', delta)
#
# delta = exp(A3, leja_points, div_diff, v=v2) -\
#         (A2*np.exp(2.0)).dot(v2)
# print('A3 v2: ', delta)
#
# delta = exp(A3, leja_points, div_diff, v=v3) -\
#         (A2*np.exp(2.0)).dot(v3)
# print('A3 v3: ', delta)
# print('--------------')


from exponentiation.exp import matrix_exp_puzzer as exp

A1 = np.matrix([
    [1., 2., 3.],
    [2., 1., -1.],
    [3., -1., 1.]])

a = exp(A1, 1.0)
print('#'*30)
print(a)
print('#'*30)
print(a.dot(a.getH()))


