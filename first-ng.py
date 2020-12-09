import numpy as np
from math import sqrt, sin, cos
from exponentiation.exp import matrix_exp_puzzer as exp
import numpy.linalg as la

a = 4.35196e4/3.0
b = 0.030553
H0 = a * np.array([
    [0., 0., 0.],
    [0., b, 0],
    [0., 0, 1]])

rad = np.pi/180
s12 = np.sin(33.62 *rad)
s23 = np.sin(27.2 * rad)
s13 = np.sin(8.53 * rad)

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
print(W)

v0 = 93536.7
n = 10.3

step = 0.01
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

print(exp(W, v1, 1), '\n', 1-la.norm(exp(W, v1, 1)))
# print(exp(W, v2, 1), '\n', (1-la.norm(exp(W, v2, 1))))
# print(exp(W, v3, 1), '\n', (1-la.norm(exp(W, v3, 1))))
# V1 = np.array([ [0.688242 + 0.570669j], [-0.207288 + 0.379438j], [-0.0561521 + 0.102786j]])
# V2 = np.array([[-0.207288 + 0.379438j], [0.862174 + 0.252289j], [-0.0373356 + 0.0683423j]])
# V3 = np.array([[-0.0561521 + 0.102786j], [-0.0373356 + 0.0683423j], [0.989886 + 0.0185132j]])
# print(1-la.norm(V1))
# print(1-la.norm(V2))
# print(1-la.norm(V3))


# def f_prof(t):
#     return v0*np.exp(-1*n*t)
#
#
# section = np.arange(0, 1+step, step)
# psi = v
# for i, t in enumerate(section):
#     print('-'*10, f' {i} ','-'*10,)
#     omega = H0 + f_prof(t) * W
#     psi = exp(-1.0*omega, psi, t) #??
#     print(psi)
#     print(la.norm(psi))
#
# #print(psi)
