import numpy as np
from math import sqrt, sin
from exponentiation.exp import matrix_exp_leja as exp


a = 123
H0 = np.array([
    [0., 0.],
    [0., a]])

c = sqrt(1-sin(0.437)**2)
W = np.array([
    [c, 1.],
    [1., c]])
v0 = 93536.7
n = 10.3

step = 0.01


def f_prof(t):
    return v0*exp(-1*n*t)


section = np.arange(0, 1+step, step)
psi = np.array([1., 0.])

for i, t in enumerate(section):
    omega = H0 + f_prof(t) * W
    psi = exp(W, section) * psi


print(psi)
