import numpy as np
from math import sqrt, sin, cos
from exponentiation.exp import matrix_exp_puzzer as exp


a = 4.35196e4/3.0
b = 0.030553
H0 = np.array([
    [0., 0., 0.],
    [0., b, 0],
    [0., 0, 1]])

rad = np.pi/180
teta12 = 33.62 *rad
teta23 = 27.2 * rad
teta13 = 8.53 * rad
W = np.array([
    [cos(teta13)**2 * cos(teta12)**2,
     cos(teta12)*sin(teta12)*cos(teta13)**2,
     cos(teta12)*cos(teta13)*sin(teta13)],

    [cos(teta12)*sin(teta12)*cos(teta13)**2,
     sin(teta12)**2 * cos(teta13)**2,
     sin(teta12)*cos(teta13)*sin(teta13)],

    [cos(teta12)*cos(teta13)*sin(teta13),
     sin(teta12)*cos(teta13)*sin(teta13),
     sin(teta13)**2]])

v0 = 93536.7
n = 10.3

step = 0.01
v = np.array([
    [1.0],
    [0.0],
    [0.0]])


def f_prof(t):
    return v0*np.exp(-1*n*t)


section = np.arange(0, 1+step, step)
psi = v
for i, t in enumerate(section):
    omega = H0 + f_prof(t) * W
    psi = exp(omega, psi, t)



print(psi)
