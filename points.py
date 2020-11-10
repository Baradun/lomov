import numpy as np
import matplotlib.pyplot as plt


def next_point(section, arr):
    maximum = -1
    # Перебираем все точки из отрезка
    for i in section:
        # произведение модулей
        p = 1.0
        for j in arr:
            p *= abs(i-j)

        if p > maximum:
            maximum = p
            point = i
    return point


def get_interpolation_points(section, points_number):

    # первая точка
    arr = [max(section)]
    # остальные точки
    for i in range(1, points_number):
        arr.append(next_point(section, arr))

    return arr


def get_points(x1, x2, number_of_points):
    step = 1/100000
    section = np.arange(x1, x2 + step, step)
    section = section.tolist()
    return get_interpolation_points(section, number_of_points)


points01 = get_points(0.0, 1.0, 30)
#print('     0 to 1: ', points01)
for i in points01:
    print('{:.3f}'.format(i), '; ', end='')
print('')


