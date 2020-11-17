import numpy as np


def matrix_exp_leja(matrix, leja_points, div_diff, v=1):

    interpolation_points = leja_points
    sum_divided_difference = div_diff[0] * v
    w = v
    for i in np.arange(1, len(interpolation_points)):
        w = matrix.dot(w) - interpolation_points[i-1] * w
        sum_divided_difference = sum_divided_difference + div_diff[i] * w
        #print(sum_divided_difference)
    return sum_divided_difference
