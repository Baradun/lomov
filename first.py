import numpy as np
from math import sqrt, sin, exp
a = 123
H0 = np.array([
    [0., 0.],
    [0., a]])

c = sqrt(1-sin(0.437)**2)
W = np.array([
    [c, 1.],
    [1., c]]) 
#v = 0
#H0 = 0
#H = H0 + v*W


t=0.01
tn = 1 #????
A = 93536.7
y = np.arange(0, 1, t)
F0 = np.array([1.0, 0.0])
for i, t in enumerate(y):
    if i == 0:
        F_f = F0
    else:
        F_f = exp(t*A*(tn+t/2)) * F_f
print(F_f)

