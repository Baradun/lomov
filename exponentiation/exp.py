import numpy as np
from time import time

def get_dev_deff(interpolation_points, i):
    if i == 1:
        return np.exp(interpolation_points[0])
    else:
        i = i - 1
        a = get_dev_deff(interpolation_points[0:i], i)
        b = get_dev_deff(interpolation_points[1:], i)
        return (a - b) / (interpolation_points[i]-interpolation_points[0])


def next_point(section, arr):
    maximum = -1
    point = 0
    # Перебираем все точки из отрезка
    for i in section:
        # произведение модулей
        p = 1.0
        for j in arr:
            p *= abs(i-j)

        if p > maximum:
            point = i
            maximum = p
            point = i

    return point


def get_interpolation_points(section, points_number):
    if str(type(section)) == "<class 'numpy.ndarray'>":
        section = section.tolist()
    t0 = time()
    # первая точка
    arr = [max(section)]
    # остальные точки
    for i in range(2, points_number):
        arr.append(next_point(section, arr))
    t = time()
    print(t-t0)
    return np.array(arr)


def matrix_exp(matrix, section, v=1):
    """
    Эта функция возвразает экспонету матрицы
    section - точки из интервала с шакгом t
    v - вектор если надо exp(maxtix)*v
    """
    interpolation_points_number = len(section) + 1
    interpolation_points = get_interpolation_points(section, interpolation_points_number)

    sum_divided_difference = get_dev_deff(interpolation_points[0:1], 1) * v
    w = v
    for i in range(1, len(section)):
        w = matrix * w - interpolation_points[i-1] * w
        sum_divided_difference = sum_divided_difference + get_dev_deff(interpolation_points[0:i+1], i+1) * w

    return sum_divided_difference
