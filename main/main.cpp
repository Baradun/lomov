#include <complex>
#include <iostream>
#include <vector>

#include <math.h>

#include </usr/include/eigen3/Eigen/Dense>

using namespace std;
//using namespace Eigen;

double f_prof( double t, double v0, double n) {
    return v0 * exp(-1 * n * t);
}

double get_lambda(double k, complex<double> p, complex<double> q){
    return cos((1.0/3.0) * acos((-3.0*q/(2.0*p))*sqrt(3.0/p)) - 2.0*M_PI*k/3.0);
}

vector<double> get_section(double start, double end, double step){
    vector<double> section;
    while(start <= end ){
        section.push_back(start);
        start += step;
    }
    return section;
} 

Eigen::Matrix <std::complex<double>, 3, 1> matrix_exp_puzzer(
    Eigen::Matrix <double, 3, 3> matrix,
    Eigen::Matrix <std::complex<double>, 3, 1> v,
    double t)
{
    Eigen::Matrix <std::complex<double>, 3, 3> I;
    I << 
    1.0, 0.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 0.0, 1.0;
    double z = matrix.trace()/3.0;
    Eigen::Matrix <double, 3, 3> matrix0 = matrix - z * I;
    
    double p = (matrix0.pow(2)).trace() * 0.5; 
    double q = matrix0.determinant();  

    auto lbd0 = get_lambda(0.0, p, q);
    auto lbd1 = get_lambda(1.0, p, q);
    auto lbd2 = get_lambda(2.0, p, q);

    double a = 2.0*sqrt(p/3.0)*(lbd1 - lbd0);
    double b = 2.0*sqrt(p/3.0)*(lbd2 - lbd0);
    double c = 2.0*sqrt(p/3.0)*(lbd1 - lbd2);

    lbd0 *= 2.0*sqrt(p/3.0);
    lbd1 *= 2.0*sqrt(p/3.0);
    lbd2 *= 2.0*sqrt(p/3.0);

    std::complex <double> j1 ( 0.0 , 1.0 );
    double r0 = -1.0*(1.0 - exp(j1*a*t))/a;
    double r1 = (-1.0/c)*(-r0-((1.0 - exp(j1*b*t))/b));

    Eigen::Matrix <std::complex<double>, 3, 1> q1 = (1 - lbd0 * (r0 - lbd1 * r1)) * v;
    Eigen::Matrix <std::complex<double>, 3, 1> psi = matrix0*v;
    Eigen::Matrix <std::complex<double>, 3, 1> q2 = (r0 + lbd2 * r1) * psi;
    Eigen::Matrix <std::complex<double>, 3, 1> q3 = r1 * matrix0*psi;

    return exp(j1 * t * z) * exp(j1 * lbd0 * t) * (q1 + q2 + q3);
}



Eigen::Matrix<std::complex<double>, 3, 3> M2(
    Eigen::Matrix <double, 3, 3> H0,
    Eigen::Matrix <double, 3, 3> W,
    Eigen::Matrix <std::complex<double>, 3, 1> v,
    double v0,
    double n,
    double start,
    double stop,
    double step)
{
    // Eigen::Matrix <std::complex<double>, 3, 3> matrixA;
    // matrixA.setZero();
    // matrixA(2,1) = std::complex <double> ( 4.0 , 5.0 );
    auto section = get_section(start, stop, step);
    Eigen::Matrix <double, 3, 3> A;
    
    for(double t: section){
        A = step*(H0 + f_prof(t +step / 2.0, v0, n) * W); //по адресу
        v = matrix_exp_puzzer(A, v, t);
    }
    
    return v;
}




int main() {
    // ----- test vectors -----
    Eigen::Matrix <std::complex<double>, 3, 1> v1;
    v1(0, 0) = 1;
    Eigen::Matrix <std::complex<double>, 3, 1> v2;
    v2(1, 0) = 1;
    Eigen::Matrix <std::complex<double>, 3, 1> v3; 
    v3(2, 0) = 1;
    // std::cout << v1 <<std::endl<<std::endl;
    // std::cout << v2 <<std::endl<<std::endl;
    // std::cout << v3 <<std::endl<<std::endl;

    



    // ----- H0 -----
    Eigen::Matrix <double, 3, 3> H0;
    H0.setZero();
    double a = 4.35196e6 / 3.0;
    double b = 0.030554;
    H0(1, 1) = a*b;
    H0(2, 2) = a;
    // std::cout << H0 <<std::endl<<std::endl;





    // ----- W -----
    double s12 = std::sqrt(0.308);
    // double s23 = std::sqrt(0.437);
    double s13 = std::sqrt(0.0234);

    double c12 = std::sqrt(1 - std::pow(s12, 2));
    // double c23 = std::sqrt(1 - std::pow(s23, 2));
    double c13 = std::sqrt(1 - std::pow(s13, 2));
    
    Eigen::Matrix <double, 3, 3> W;
    W  << 
    pow(c13, 2) * pow(c12, 2),   c12 * s12 * pow(c13, 2),    c12 * c13 * s13,
    c12 * s12 * pow(c13, 2),     pow(s12, 2) * pow(c13, 2),  s12 * c13 * s13,
    c12 * c13 * s13,             s12 * c13 * s13,            pow(s13, 2);
    // std::cout << W <<std::endl<<std::endl;
    
    



    // ----- other -----
    double v0 = 93536.7;
    double n = 10.3;

    double start = 0.0;
    double stop = 1.0;
    double step = 0.1;
    std::cout << M2(H0, W, v1, v0, n, start, stop, step) << std::endl; //по адресу передать 
    return 0;
}