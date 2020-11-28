#!/usr/bin/env python

import numpy as np
from numpy import linalg as la
import os as os

def m_exp(matrix, leja_points, div_diff, v, order):
    expAv = div_diff[0] * v
    w = v
    delta = 0.
    for i in np.arange(1, order):
        w = matrix.dot(w) - leja_points[i-1] * w
        expAv = expAv + div_diff[i] * w
        delta = div_diff[i+1]*w
    return expAv, delta

### We presume that test directory contains two data files:
### 'lb-Bb_N#.dat' where B=l|r and # --- number of precomputer Leja points
### and 'ddef-Bb_N#.dat'. Both contains float number in binary form.

### for future enhancement: to choose at script run.
N = 500
branch = 'l'
lj_dat = 'lp-{}b_N{}.dat'.format(branch, N)
dd_dat = 'ddef-{}b_N{}.dat'.format(branch, N)

with open(lj_dat, "rb") as f:
    lj_ps = np.fromfile(f, dtype=np.dtype(np.float64))

with open(dd_dat, "rb") as f:
    ddef = np.fromfile(f, dtype=np.dtype(np.float64))

if len(lj_ps) != N:
    print("Data file with Leja points is corrupted.")
    print("We expected to get {} points but file has different number of them.".format(N))
    os.exit(1)

sg3 = np.array([ [1., 0.], [0., -1.]])
I = np.array([[1., 0.], [0., 1.]])

### Tests matrices.

A1 = np.array([
    [1., 2.],
    [0., 1.]])
### exp^{A1} = e A1
expA1 = np.exp(1)*A1
#####################################################################
A2 = np.array([ [1., 2.], [-1., -1.] ])
### exp^{A2} = cos(1) + A2 * sin(1)
expA2 = np.cos(1)*I + np.sin(1)*A2
#####################################################################
A3 = np.array([
    [1., 4.],
    [0., -1.]])
### exp^{A3} = ch(1) + A2 sh(1)
expA3 = np.cosh(1)*I + np.sinh(1)*A3
#####################################################################
A4 = np.array([
    [1., -1.],
    [1., 3.]])
### exp^{A4} = e^{2} np.array([[0., -1.], [1., 2.]])
expA4 = np.exp(2)*np.array([[0., -1.], [1., 2.]])
#####################################################################
A5 = np.array([[1., 0.], [0., 2.]])
### exp^{A5} = e^{3/2} (ch(1/2) + \sigma_{3} sh(1/2) )
expA5 = np.exp(1.5)*np.cosh(0.5)*I + np.exp(1.5)*np.sinh(0.5)*sg3
#####################################################################
expAs = [ expA1, expA2, expA3, expA4, expA5 ]

### Test vectors.

v1 = np.array([1., 0.])
v2 = np.array([0., -1.])
v3 = np.array([1., 2.])
v4 = np.array([2., 3.])

### Order of interpolation
m = 100

if m > N:
    print("The order of interpolation {} is higher than number of precalculated Leja points {}!".format(m, N))
    os.exit(2)

### We compute:
### exact result of exp^{A}v
### approximate result, using m Leja points,
### they delta and next term in approximation.

# --- First mtrx ---

i = 0
for A in A1, A2, A3, A4, A5:
    for v in v1, v2, v3, v4:
        print(80*"#")
        print("Array: ", A)
        print("vector: ", v)
        print("DEBUG: exp^{A} = ", expAs[i])
        expAv = expAs[i].dot(v)
        ip_expAv,dlt = m_exp(A, lj_ps, ddef, v, m)
        delta = expAv - ip_expAv
        print("exp^{A}v = ", expAv)
        print("approx exp^{A}v = ", ip_expAv)
        print("||delta|| = ", la.norm(delta))
        print("next term approx. = ", la.norm(dlt))
    i = i+1
