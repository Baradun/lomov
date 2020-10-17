import numpy as np
from math import sqrt, sin
a = 123
H0 = np.array([
    [0., 0.],
    [0., a]])

c = sqrt(1-sin(0.437)**2)
W = np.array([
    [c, 1.],
    [1., c]]) 


def get_v(step, t):
    v0 = 93536.7
    n = 10.3

    tn = step*t
    v = v0 * np.exp(-1*n*tn)
    return v

t=0.01
y = np.arange(0, 1, t)
F0 = np.array([1.0, 0.0])
psi = np.array([1.,0.])

for i, t in enumerate(y):
    omega = H0 + get_v(i, t) * W
    psi = np.exp(omega) * psi

print(psi)

