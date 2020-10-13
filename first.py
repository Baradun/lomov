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


def get_A(step, t, A=None):
    if A is None:
        v0 = 93536.7
        n = 10.3
        v = v0 * np.exp(-1*n*t) #??
        A = H0 + v*W
        return A
    
    tn = step*t 
    A = np.exp(t*A*(tn+t/2))
    return A

t=0.01
y = np.arange(0, 1, t)
F0 = np.array([1.0, 0.0])

for i, t in enumerate(y):
    if i == 0:
        A = get_A(i,t)
    else:
        A = H0 + get_A(i,t,A)* W

print(A)

