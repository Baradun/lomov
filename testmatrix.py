from exponentiation.exp import matrix_exp
import numpy as np

step = 1/10
section = np.arange(0, 1+step, step)

A1 = np.array([
    [1., 2.],
    [0., 1.]])
v = np.array([1., 0.])
print(matrix_exp(A1, section, v))

A2 = np.array([
    [1., 2.],
    [-1., -1.]])

print(matrix_exp(A2, section))
