import numpy as np


def get_dev_deff(interpolation_points, i):
    pass


def next_point(section, arr):
    maximum = -1
    point = 0
    # Перебираем все точки из отрезка
    for i in section:
        # произведение модулей
        p = 1
        for j in arr:
            p *= abs(i-arr[j])

        if p > maximum:
            point = i
            maximum = p
    return point


def get_interpolation_points(section, points_number):

    # первая точка
    arr = [max(section)]
    # остальные точки
    for i in range(2, points_number):
        arr.append(next_point(section, arr))
    return arr


def matrix_exp(matrix, section, v=1):
    """
    Эта функция возвразает экспонету матрицы
    section - точки из интервала с шакгом t
    v - вектор если надо exp(maxtix)*v
    """
    interpolation_points_number = 10
    interpolation_points = get_interpolation_points(section, interpolation_points_number)

    sum_divided_difference = get_dev_deff(interpolation_points, 0) * v
    w = v
    for i in range(1, len(section)):
        w = matrix * w - interpolation_points[i - 1] * w
        sum_divided_difference = sum_divided_difference + get_dev_deff(interpolation_points, i) * w

    return sum_divided_difference
