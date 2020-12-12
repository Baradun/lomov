import numpy as np
from math import sqrt, sin, cos
from exponentiation.exp import matrix_exp_puzzer as exp
import numpy.linalg as la

a = 4.35196e4/3   # 6 степень
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


v0 = 93536.7
n = 10.3

step = 0.001
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

e1 = exp(W, v1, 1)
e2 = exp(W, v2, 1)
e3 = exp(W, v3, 1)
print(e1, '\n', "norm1", 1-la.norm(e1))
print(e2, '\n', "norm2", 1 - la.norm(e2))
print(e3, '\n', "norm3", 1-la.norm(e3))

#
#
# V1 = np.array([[0.688242 + 0.570669j], [-0.207288 + 0.379438j], [-0.0561521 + 0.102786j]])
# V2 = np.array([[-0.207288 + 0.379438j], [0.862174 + 0.252289j], [-0.0373356 + 0.0683423j]])
# V3 = np.array([[-0.0561521 + 0.102786j], [-0.0373356 + 0.0683423j], [0.989886 + 0.0185132j]])
# print(1-la.norm(V1))
# print(1-la.norm(V2))
# print(1-la.norm(V3))

#e1 = exp(H0 + W, v1, 1)
#print(e1, '\n', "norm1", 1-la.norm(e1))

def f_prof(t):
    return v0*np.exp(-1*n*t)


section = np.arange(0, 1+step, step)
psi = v1
for i, t in enumerate(section):
    print('-'*10, f' {i} ','-'*10,)
    omega = H0 + f_prof(t) * W
    psi = exp(omega, psi, t) #??
    print(psi)
    print(la.norm(psi))

print(psi)
