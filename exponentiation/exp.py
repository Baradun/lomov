import numpy as np
import numpy.linalg as la


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

    #print('matrix0', matrix0)

    p = np.trace(matrix0.dot(matrix0))*0.5
    # p = -1.0/3.0
    q = -la.det(matrix0)
    # print('p,q', p, q)

    def get_lambda(k):
        solve = np.cos((1/3)*np.arccos((-3*q/(2*p))*np.sqrt(3./p)) - 2*np.pi*k/3)
        return solve

    ls = np.sort(np.array([get_lambda(0.0), get_lambda(1.0), get_lambda(2.0)]))

    # print('lbd1 - lbd0', ls[1] - ls[0])
    # print('lbd2 - lbd0', ls[2] - ls[0])
    # print('lbd1 - lbd2', ls[1] - ls[2])

    a = 2*np.sqrt(p/3)*(ls[1] - ls[0])
    b = 2*np.sqrt(p/3)*(ls[2] - ls[0])
    c = 2*np.sqrt(p/3)*(ls[1] - ls[2])

    ls = ls * 2*np.sqrt(p/3)
    lbd0 = ls[0]
    lbd1 = ls[1]
    lbd2 = ls[2]

    #r0 = -1*(np.sin(a/2*t)**2 - 1j*np.sin(a*t))/a
    r0 = -1*(1.0 - np.exp(1j*a*t))/a
    r1 = (-1.0/c)*(-r0-((1.0 - np.exp(1j*b*t))/b)) #????????????????????
    #print('??', -r0-((1.0 - np.exp(1j*b*t))/b))

    #print('a,b,c', a, b, c)
    #print('r0,r1', r0, r1)

    #print('\n')
    #print('check roots of equation', '\n')



    def calc(y):
        return y**3 + p*y + q

    # print('lb:', lbd0, lbd1, lbd2)
    # print('lbd0', calc(lbd0))
    # print('lbd1', calc(lbd1))
    # print('lbd2', calc(lbd2))
    # print('sum', lbd0 + lbd1 + lbd2)
    # print('pr', lbd0*lbd1*lbd2)
    # print('sumpr', lbd0*lbd1 + lbd0*lbd2 + lbd1*lbd2)
    # print('\n')



    #q1 = np.exp(1j*t*z)*I
    #q2 = np.exp(1.0j*lbd0*t)*((1.0-lbd0*(r0-lbd1*r1))*I + (r0+lbd2*r1)*matrix0 + r1*matrix0.dot(matrix0))

    #print('q1', q1)
    #print('q2', q2)
    #return (q1*q2).dot(v)
    q1 = (1 - lbd0 * (r0 - lbd1 * r1)) * v
    psi = matrix0.dot(v)
    q2 = (r0 + lbd2 * r1) * psi
    q3 = r1 * matrix0.dot(psi)
    # print('q1', q1)
    # print('q2', q2)
    # print('q3', q3)
    # print('psi', psi)
    # print('#' * 50)
    return np.exp(1j * t * z) * np.exp(1j * lbd0 * t) * (q1 + q2 + q3)

