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


    p = np.trace(matrix0.dot(matrix0))*0.5
    q = la.det(matrix0)
    print('p,q', p, q)

    def get_lambda(k):
        solve = np.cos((1/3)*np.arccos((3*q/(2*p))*np.sqrt(3./p)) - 2*np.pi*k/3)
        return solve

    lbd0 = get_lambda(0.0)
    lbd1 = get_lambda(1.0)
    lbd2 = get_lambda(2.0)

    a = lbd1 - lbd0
    b = lbd2 - lbd0
    c = lbd1 - lbd2
    a *= 2.0*np.sqrt(p/3.0)
    b *= 2.0*np.sqrt(p/3.0)
    c *= 2.0*np.sqrt(p/3.0)


    lbd0 *= 2*np.sqrt(p/3)
    lbd1 *= 2*np.sqrt(p/3)
    lbd2 *= 2*np.sqrt(p/3)
    
    print('lbd0=',lbd0, ' lbd1=',lbd1, ' lbd2=',lbd2)
    
    # r0 = -1.0*(1.0 - np.exp(1j*a*t))/a
    # r1 = (-1.0/c)*(-r0-((1.0 - np.exp(1j*b*t))/b))

    r0 = -1.0*(2.0*np.sin(a/2.)*np.sin(a/2.) - 1j*np.sin(a))/a
    r1 = -1.0/c*(-r0 - (2.0 * np.sin(b/2.0) * np.sin(b/2.0) - 1j *np.sin(b))/b)

    print('a=', a,' b=' ,b,' c=' ,c)
    print('r0=', r0, ' r1=', r1)

    print('\n')
    print('check roots of equation', '\n')



    def calc(y):
        return y**3 + p*y + q

    print('lb:', lbd0, lbd1, lbd2)
    print('lbd0', calc(lbd0))
    print('lbd1', calc(lbd1))
    print('lbd2', calc(lbd2))
    print('sum', lbd0 + lbd1 + lbd2)
    print('pr', lbd0*lbd1*lbd2)
    print('sumpr', lbd0*lbd1 + lbd0*lbd2 + lbd1*lbd2)
    print('\n')


    q1 = (1 - lbd0 * (r0 - lbd1 * r1)) * v
    psi = matrix0.dot(v)
    q2 = (r0 + lbd2 * r1) * psi
    q3 = r1 * matrix0.dot(psi)
    
    # print('q1', q1)
    # print('q2', q2)
    # print('q3', q3)
    # print('psi', psi)
    return np.exp(1j * t * z) * np.exp(1j * lbd0 * t) * (q1 + q2 + q3)

