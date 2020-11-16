#!/usr/bin/env python

import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt
import os as os

a = 0.0
b = 1.0

def f_LP(x, n, ps):
    """ Returns value of Leja points function for order n.

    Arguments:
      x --- a point in range [0;1];
      n --- order (multiplication of n factors);
      ps --- array of calculated Leja points.
    """
    p = 1
    if len(ps) < n:
        print("Error: number of points is less than order!")
        return nil
    for k in np.arange(n):
        p = p*(x-ps[k])
    return np.abs(p)

def draw_LP(n,ps):
    x = np.linspace(a,b,500)
    y = [f_LP(k, n, ps) for k in x]
    xn = ps[n]
    yn = f_LP(xn, n, ps)
    plt.plot(x,y,xn,yn,r'*')

def fLP(x, ps):
    """ Returns value of Leja points function.

    Takes two arguments:
      x --- a point (in range [0;1]);
      ps --- array of previously found Leja points.
    """
    p=1
    for k in ps:
        p = p*(x-k)
    return np.abs(p)

def diff(x, d, ps):
    """ Calculate numerical derivative for Leja points function.

    Arguments:
      x --- a point;
      d --- delta for numerical derivative;
      ps --- array of previously calculated Leja points.
    """
    return (fLP(x+d,ps) - fLP(x-d,ps))/(2*d)

def find_max(a, b, ps, d, e):
    """ Finds maximum value of Leja points function in given range.

    Arguments:
      a,b --- left and right edges of range;
      ps --- array of previosly calculated Leja points;
      d --- delta to calculate numeric derivative;
      e --- "epsilon", when we consider that value is a "zero".
    """
    c  = 0.5*(a+b)
    if np.abs(b-a) < 2*e:
        return -1,-1
    if d > 0.5*(b-a):
        print("WARNING: we have to decrease delta from {} to value {} but this is suboptimal and would increase errors.".format(d,0.25*(b-a)))
        os.exit(2)
        d = 0.25*(b-a)
    fd = diff(c, d, ps)
    if np.abs(fd) < e:
        return c, fLP(c, ps)
    if fd > 0:
        return find_max(c, b, ps, d, e)
    elif fd < 0:
        return find_max(a, c, ps, d, e)

def calc_LP(e, d, n, ser):
    """ Calculate n Leja points with given precision.

    Arguments:
      e --- "epsilon", when we consider that value is a "zero";
      d --- delta, to compute numeric derivative;
      n --- number of found Leja points;
      ser --- a branch.

    The Leja points by definiton have interesting property. We consider range
    [0;1], the first three points are easily calculated: 1, 0 and 0.5. The
    fourth point being maximum of Leja points function has two possible
    variants: the Leja points function has two extrema of equal value, the
    maxima points are symmetric around point 0.5. Choosing left point (relative
    to 0.5) we left branch of Leja points, choosing right point we obtain
    the right branch Leja points.
    """
    ps = np.array([1.0, 0.0, 0.5])
    sps = np.sort(ps)
    if ser == 1:
        x, v = find_max(sps[0], sps[1], ps, d, e)
    else:
        x, v = find_max(sps[1], sps[2], ps, d, e)
    ps = np.append(ps, x)

    for i in np.arange(3,n-1):
        mx = np.array([])
        mv = np.array([])
        sps = np.sort(ps)
        for k in np.arange(i):
            x, v = find_max(sps[k], sps[k+1], ps, d, e)
            if x > 0:
                mx = np.append(mx, x)
                mv = np.append(mv, v)
        point = mx[np.argmax(mv)]
        val   = mv[np.argmax(mv)]
        ps = np.append(ps, point)
    return ps

# relation between delta and epsilon: delta \approx epsilon^{1/3}
epsilon = 1e-15
delta   = 1e-5
N       = 127
N       = 30

points = calc_LP(epsilon, delta, N, 1)
print(points)
points.tofile(pl.Path("lp-lbN{}.dat".format(N)))
points = calc_LP(epsilon, delta, N, 2)
#  print(points)
points.tofile(pl.Path("lp-rbN{}.dat".format(N)))
### To read data:
# dt=np.dtype(np.float64)
# a = np.fromfile(pl.Path("file"), dtype=dt)
