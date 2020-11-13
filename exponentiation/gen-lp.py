import numpy as np
from time import time

a = 0.0
b = 1.0


def fLP(x, ps):
    p = 1
    for k in ps:
        p = p*(x-k)
    return np.abs(p)


def diff(x, d, points_arr):
    return (fLP(x + d, points_arr) - fLP(x - d, points_arr)) / (2 * d)


def find_max(a, b, points_arr, d, e):
    c = 0.5*(a+b)
    if np.abs(b-a) < 2*e:
        return -1, -1
    if d > 0.5*(b-a):
        d = 0.25*(b-a)  # ???
    fd = diff(c, d, points_arr)
    if np.abs(fd) < e:
        return c, fLP(c, points_arr)
    if fd > 0:
        return find_max(c, b, points_arr, d, e)
    elif fd < 0:
        return find_max(a, c, points_arr, d, e)


def calc_LP(e, d, n):
    points_arr = np.array([0.0, 1.0, 0.5])
    for i in np.arange(2, n):

        m = np.array([[0, 0]])
        pts = np.linspace(a, b, i+1)
        for j in np.arange(i):
            x, v = find_max(pts[j], pts[j+1], points_arr, d, e)
            if x > 0:
                m = np.append(m, [[x, v]], axis=0)
        point = m[np.argmax(m, axis=0)][1, 0]

        points_arr = np.append(points_arr, point)
    return points_arr


epsilon = 1e-10
delta = 1e-5
N = 100

t0 = time()
points = calc_LP(epsilon, delta, N)
t = time()
print(points)
print('time:', t-t0)
