import asyncio
from time import time

import numpy as np
from math import sqrt, sin, cos
from exponentiation.exp import matrix_exp_puzzer as exp
import numpy.linalg as la

a = 4.35196e2/3   # 6 степень
b = 0.030554
H0 = a * np.array([
    [0., 0., 0.],
    [0., b, 0],
    [0., 0, 1]])

s12 = np.sqrt(0.308)
s23 = np.sqrt(0.437)
s13 = np.sqrt(0.0234)

c12 = np.sqrt(1 - s12**2)
c23 = np.sqrt(1 - s23**2)
c13 = np.sqrt(1 - s13**2)


W = np.array([
    [c13**2 * c12**2,
     c12 * s12 * c13**2,
     c12 * c13 * s13],

    [c12 * s12 * c13**2,
     s12**2 * c13**2,
     s12 * c13 * s13],

    [c12 * c13 * s13,
     s12 * c13 * s13,
     s13**2]])
# print(W)



v1 = np.array([
    [1.0],
    [0.0],
    [0.0]])
v2 = np.array([
    [0.0],
    [1.0],
    [0.0]])
v3 = np.array([
    [0.0],
    [0.0],
    [1.0]])
#
# e1 = exp(W, v1, 1)
# e2 = exp(W, v2, 1)
# e3 = exp(W, v3, 1)
# print(e1, '\n', "norm1", 1-la.norm(e1))
# print(e2, '\n', "norm2", 1 - la.norm(e2))
# print(e3, '\n', "norm3", 1-la.norm(e3))

#
# print(1-la.norm(V1))
# print(1-la.norm(V2))
# print(1-la.norm(V3))
H1 = np.array([[ 0.51, 1.25, -4.7],
              [1.25,-10.71, 2.74],
              [-4.7, 2.74, 1.53]])
H2 = np.array([[1.15, -1.27 + 0.76j, 7.41],
               [-1.27 - 0.76j, 4.4, 5.2 - 2.6],
            [7.41, 5.2 + 2.6j, 1.23 ]])

H3 = np.array([[ 0.0, sqrt(2.) - 0.5j, sqrt(3.)],
            [sqrt(2.) + 0.5j, 0.0, -0.5 - 0.5j*sqrt(3.)],
         [sqrt(3.), -0.5 + 0.5j*sqrt(3.), -1.0 ]])

e1 = exp(H1, v1, 1)
e2 = exp(H1, v2, 1)
e3 = exp(H1, v3, 1)
print(e1, '\n', "norm1", 1-la.norm(e1))
print(e2, '\n', "norm2", 1 - la.norm(e2))
print(e3, '\n', "norm3", 1-la.norm(e3))
# print(e1, '\n', "norm1", 1-la.norm(e1))




#
def M2(H0, W, v, step):
    v0 = 93536.7
    n = 10.3

    def f_prof(t):
        return v0 * np.exp(-1 * n * t)

    section = np.arange(0, 1+step, step)
    Y = v
    for i, t in enumerate(section):
        print('-'*10, f' {i} ', '-'*10,)
        A = step*(H0 + f_prof(t+step/2) * W)
        Y = exp(A, Y, t)
        print(Y)
        print('norm ', la.norm(Y))

    print('-'*10, ' final ', '-'*10,)
    print(Y)
    #return Y


#M2(H0, W, v1, 0.01)
#
#
#
#
# ###################################################
def M4(H0, W, v, step):
    v0 = 93536.7
    n = 10.3

    def f_prof(t):
        return v0 * np.exp(-1 * n * t)

    def commutator(A1, A2):
        return A1.dot(A2) - A2.dot(A1)

    section = np.arange(0, 1 + step, step)
    Y = v
    c1 = 0.5 - np.sqrt(3)/6
    c2 = 0.5 + np.sqrt(3)/6
    for i, t in enumerate(section):
        print('-'*10, f' {i} ', '-'*10,)
        A1 = H0 + f_prof(t + c1*step) * W
        A2 = H0 + f_prof(t + c2*step) * W
        omega = step/2*(A1+A2) + (np.sqrt(3)/12 * step**2) * commutator(A2, A1)
        Y = exp(omega, Y, t)
        print(Y)
        print('norm ', la.norm(Y))

    print('-'*10, ' final ', '-'*10,)
    print(Y)
    return Y
#
M4(H0, W, v1, 0.0001)
# t = time()
# matrM2 = M2(H0, W, v1, 0.00001)
# matrM4 = M4(H0, W, v1, 0.00001)
#
# print('#' * 80)
# print('M2:\n', matrM2)
# print('norm ', la.norm(matrM2))
#
# print('M4:\n', matrM4)
# print('norm ', la.norm(matrM4))
# print('delta:\n', matrM2 - matrM4)
# print('t:', time() - t)

def M6(H0, W, v, step):
    v0 = 93536.7
    n = 10.3

    def f_prof(t):
        return v0 * np.exp(-1 * n * t)

    def commutator(A1, A2):
        return A1.dot(A2) - A2.dot(A1)

    section = np.arange(0, 1 + step, step)
    Y = v
    c1 = 0.5 - np.sqrt(15)/10
    c2 = 0.5
    c3 = 0.5 + np.sqrt(15)/10
    for i, t in enumerate(section):
        print('-'*10, f' {i} ', '-'*10,)
        A1 = H0 + f_prof(t + c1 * step) * W
        A2 = H0 + f_prof(t + c2 * step) * W
        A3 = H0 + f_prof(t + c3 * step) * W
        B1 = step * A2
        B2 = (np.sqrt(15)*step/3)*(A3-A1)
        B3 = (10*step/3)*(A3 - 2*A2 + A1)
        omega = B1 + 0.5*B3 + 1/240*commutator(-20*B1-B3+commutator(B1, B2), B2 - 1/60*commutator(B1, 2*B3+ commutator(B1, B2)))
        Y = exp(omega, Y, t)
        print(Y)
        print('norm ', la.norm(Y))

    print('-'*10, ' final ', '-'*10,)
    print(Y)
    return Y

#M6(H0, W, v1, 0.0001)
################################################################


def Cf4(H0, W, v, step):
    v0 = 93536.7
    n = 10.3

    def f_prof(t):
        return v0 * np.exp(-1 * n * t)

    section = np.arange(0, 1 + step, step)
    Y = v
    c1 = 0.5 - np.sqrt(3) / 6
    c2 = 0.5 + np.sqrt(3) / 6
    alfa1 = (3 - 2 * np.sqrt(3)) / 12
    alfa2 = (3 + 2 * np.sqrt(3)) / 12
    for i, t in enumerate(section):
        print('-'*10, f' {i} ', '-'*10,)
        A1 = H0 + f_prof(t + c1 * step) * W
        A2 = H0 + f_prof(t + c2 * step) * W
        omega = 123 #???????????????????
        Y = exp(omega, Y, t)
        print(Y)
        print('norm ', la.norm(Y))

    print('-'*10, ' final ', '-'*10,)
    print(Y)
    return Y