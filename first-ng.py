import numpy as np
from math import sqrt, sin, exp
from exponentiation.exp import matrix_exp


a = 123
H0 = np.array([
    [0., 0.],
    [0., a]])

c = sqrt(1-sin(0.437)**2)
W = np.array([
    [c, 1.],
    [1., c]]) 
step = 0.01
v0 = 93536.7
n = 10.3


def f_prof(t):
    return v0*exp(-1*n*t)


def get_v(step, t):
    v0 = 93536.7
    n = 10.3

    tn = step*t
    v = v0 * np.exp(-1*n*tn)
    return v


section = np.arange(0, 1+step, step)
psi = np.array([1., 0.])

for i, t in enumerate(section):
    omega = H0 + f_prof(t) * W
    psi = matrix_exp(W, section) * psi


print(psi)
