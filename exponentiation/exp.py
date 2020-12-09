import numpy as np
import numpy.linalg as la
from math import sqrt, exp

def matrix_exp_leja(matrix, leja_points, div_diff, number_points, v=1):

    interpolation_points = leja_points[0:number_points]
    sum_divided_difference = div_diff[0] * v
    #print(sum_divided_difference)
    w = v
    for i in np.arange(1, number_points):
        #print(f'{i} ', matrix.dot(w))
        w = matrix.dot(w) - interpolation_points[i-1] * w
        sum_divided_difference = sum_divided_difference + div_diff[i] * w
    return sum_divided_difference


def matrix_exp_puzzer(matrix, v, t):
    I = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]])
    z = np.trace(matrix)/3.0
    matrix0 = matrix - z * I
    p = np.trace(matrix0.dot(matrix0))*0.5
    q = la.det(matrix0)
    print('p,q', p ,q)
    def get_lambda(k):
        solve = np.cos((1/3)*np.arccos((3*q/(2*p))*np.sqrt(3./p)) - 2*np.pi*k/3)
        return solve

    ls = np.sort(np.array([get_lambda(0.0), get_lambda(1.0), get_lambda(2.0)]))
    lbd0 = ls[0]
    lbd1 = ls[1]
    lbd2 = ls[2]

    a = 2*np.sqrt(p/3)*(lbd1 - lbd0)
    b = 2*np.sqrt(p/3)*(lbd2 - lbd0)
    r0 = -1*(np.sin(a/2  *t)**2 - 1j*np.sin(a*t))/a
    r1 = (-1.0/(a-b))*(-r0-((1.0 - np.exp(1j*b*t))/b))
    print('ls', ls)
    print('a,b', a, b)
    print('r0,r1', r0, r1)
    q1 = np.exp(1j*t*z)
    q2 = np.exp(1.0j*lbd0*t)
    # q3 = (1.0-lbd0*(r0-lbd1*r1))*I + (r0+lbd2*r1)*matrix0 + r1*matrix0.dot(matrix0)
    q31 = (1.0-lbd0*(r0-lbd1*r1))*I
    q32 = (r0+lbd2*r1)*matrix0
    q33 = r1*matrix0.dot(matrix0)
    return (q1*q2*(q31+q32+q33)).dot(v)
