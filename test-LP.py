from exponentiation.exp import get_interpolation_points
from exponentiation.gen_LP import calc_LP
import numpy as np

from time import time
epsilon = 1e-10
delta = 1e-5
N = 500

t0 = time()
arr1 = calc_LP(epsilon, delta, N)
t = time()
print(t-t0)
#print(arr1)

step = 1/N
section = np.arange(0, 1+step, step)


#arr2 = get_interpolation_points(section, N)
#print(arr2)

#for i in range(len(arr1)-1):
    #print(arr1[i]-arr2[i])