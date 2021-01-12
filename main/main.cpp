#include <cmath>
#include <complex>
#include <functional>
#include <iostream>
#include <vector>

#include </usr/include/eigen3/Eigen/Dense>


using std::vector;
using std::complex;
using std::function;

using Eigen::Matrix;



double f_prof( double t, double v0, double n) {
    return v0 * exp(-n * t);
}


class Methods{

public:
    Methods(
        Matrix <double, 3, 3> H0,
        Matrix <double, 3, 3> W,
        Matrix <complex<double>, 3, 1> v,
        double v0,
        double n,
        function<double(double, double, double)> prof
    ){
        this->H0 = H0;
        this->W = W;
        this->v = v;
        this->v0 = v0;
        this->n = n;
        this->start = 0;
        this->stop  = 1;
        this->step = 0.1;
        this->prof = prof;
        set_section(start, stop, step);
    }


    Methods(
        Matrix <double, 3, 3> H0,
        Matrix <double, 3, 3> W,
        Matrix <complex<double>, 3, 1> v,
        double v0,
        double n,
        function<double(double, double, double)> prof,
        double start,
        double stop,
        double step
        
    ){
        this->H0 = H0;
        this->W = W;
        this->v = v;
        this->v0 = v0;
        this->n = n;
        this->start = start;
        this->stop  = stop;
        this->step = step;
        this->prof = prof;
        set_section(start, stop, step);
    }


    void set_section(double start, double end, double step){
        while(start <= end ){
            section.push_back(start);
            start += step;
        }
    }


    Matrix <complex<double>, 3, 1> M2(){
        Matrix <double, 3, 3> A;
        auto Y = v;
        for(double t: section){
            A = step*(H0 + prof(t + step/2.0, v0, n) * W);
            Y = matrix_exp_puzzer(A, Y, t);
        }
        return Y;
    }


    Matrix <complex<double>, 3, 1> M4(){
        auto Y = v;
        double c1 = 0.5 - sqrt(3.0)/6.0;
        double c2 = 0.5 + sqrt(3.0)/6.0;
        Matrix <double, 3, 3> A1;
        Matrix <double, 3, 3> A2;
        Matrix <double, 3, 3> omega;
        for(double t: section){
            A1 = H0 + prof(t + c1*step, v0, n) * W;
            A2 = H0 + prof(t + c2*step, v0, n) * W;
            omega = (step/2.0)*(A1+A2) + (sqrt(3.0)/12.0 * step*step) * calc_commutator(A2, A1);
            Y = matrix_exp_puzzer(omega, Y, t);
        }
        
        return Y;
    }


    Matrix <complex<double>, 3, 1> M6(){
        auto Y = v;
        double c1 = 0.5 - sqrt(15.0)/10.0;
        double c2 = 0.5;
        double c3 = 0.5 + sqrt(15.0)/10.0;
        
        Matrix <double, 3, 3> A1;
        Matrix <double, 3, 3> A2;
        Matrix <double, 3, 3> A3;
        
        Matrix <double, 3, 3> B1;
        Matrix <double, 3, 3> B2;
        Matrix <double, 3, 3> B3;
        
        Matrix <double, 3, 3> omega;
        
        for(double t: section){
            A1 = H0 + prof(t + c1 * step, v0, n) * W;
            A2 = H0 + prof(t + c2 * step, v0, n) * W;
            A3 = H0 + prof(t + c3 * step, v0, n) * W;
            
            B1 = step * A2;
            B2 = (sqrt(15.0)*step/3.0)*(A3-A1);
            B3 = (10.0*step/3.0)*(A3 - 2.0*A2 + A1);
            
            omega = B1 + 0.5*B3 + 1.0/240.0 *calc_commutator(-20.0*B1-B3+calc_commutator(B1, B2), B2 - 1.0/60.0*calc_commutator(B1, 2.0*B3+ calc_commutator(B1, B2)));
            Y = matrix_exp_puzzer(omega, Y, t);
        }
        return Y;
    }


private:
    Matrix <double, 3, 3> H0;
    Matrix <double, 3, 3> W;
    Matrix <complex<double>, 3, 1> v;
    double v0;
    double n;
    double start;
    double stop;
    double step;
    vector<double> section;
    function<double(double, double, double)> prof; //??
    

    double calc_lambda(double k, double p, double q){ 
        return cos((1.0/3.0) * acos((3.0*q/(2.0*p))*sqrt(3.0/p)) - 2.0*M_PI*k/3.0);
    }
    
    Matrix <complex<double>, 3, 1> matrix_exp_puzzer(
        Matrix <double, 3, 3> matrix,
        Matrix <complex<double>, 3, 1> vectr,
        double t)
    {
        Matrix <double, 3, 3> I;
        I << 
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0;
        double z = matrix.trace()/3.0;
        Matrix <double, 3, 3> matrix0 = matrix - z * I;
        
        double p = (matrix0*matrix0).trace() * 0.5; 
        double q = matrix0.determinant();  

        auto lbd0 = calc_lambda(0.0, p, q);
        auto lbd1 = calc_lambda(1.0, p, q);
        auto lbd2 = calc_lambda(2.0, p, q);

        double a = 2.0*sqrt(p/3.0)*(lbd1 - lbd0);
        double b = 2.0*sqrt(p/3.0)*(lbd2 - lbd0);
        double c = 2.0*sqrt(p/3.0)*(lbd1 - lbd2);

        lbd0 *= 2.0*sqrt(p/3.0);
        lbd1 *= 2.0*sqrt(p/3.0);
        lbd2 *= 2.0*sqrt(p/3.0);

        complex <double> j1 ( 0.0 , 1.0 );
        complex <double> r0 = -1.0*(1.0 - exp(j1*a*t))/a;
        complex <double> r1 = (-1.0/c)*(-r0-((1.0 - exp(j1*b*t))/b));

        Matrix <complex<double>, 3, 1> q1 = (1.0 - lbd0 * (r0 - lbd1 * r1)) * vectr;
        Matrix <complex<double>, 3, 1> psi = matrix0*vectr;
        Matrix <complex<double>, 3, 1> q2 = (r0 + lbd2 * r1) * psi;
        Matrix <complex<double>, 3, 1> q3 = r1 * matrix0*psi;

        return exp(j1 * t * z) * exp(j1 * lbd0 * t) * (q1 + q2 + q3);
    }

    Matrix <double, 3, 3> calc_commutator(
        Matrix <double, 3, 3> A,
        Matrix <double, 3, 3> B
    ){
        return A*B - B*A;
    }

};

int main() {
    // ----- test vectors -----
    Matrix <std::complex<double>, 3, 1> v1;
    v1(0, 0) = 1.0;
    Matrix <std::complex<double>, 3, 1> v2;
    v2(1, 0) = 1.0;
    Matrix <std::complex<double>, 3, 1> v3; 
    v3(2, 0) = 1.0;


    // ----- H0 -----
    Matrix <double, 3, 3> H0;
    H0.setZero();
    double a = 4.35196e6 / 3.0;
    double b = 0.030554;
    H0(1, 1) = a*b;
    H0(2, 2) = a;



    // ----- W -----
    double s12 = std::sqrt(0.308);
    // double s23 = std::sqrt(0.437);
    double s13 = std::sqrt(0.0234);
    double c12 = std::sqrt(1.0 - std::pow(s12, 2));
    // double c23 = std::sqrt(1 - std::pow(s23, 2));
    double c13 = std::sqrt(1.0 - std::pow(s13, 2));

    Eigen::Matrix <double, 3, 3> W;
    W  << 
    c13*c13 * c12*c12,     c12 * s12 * c13*c13,   c12 * c13 * s13,
    c12 * s12 * c13*c13,   s12*s12 * c13*c13,     s12 * c13 * s13,
    c12 * c13 * s13,       s12 * c13 * s13,       s13*s13;

    // ----- other -----
    double v0 = 93536.7;
    double n = 10.3;

    Methods test = Methods(H0, W, v1, v0, n, f_prof);
    test.set_section(0.0, 1.0, 0.1);
    auto v = test.M2(); 

    std::cout << 1.0 - test.M2().norm() << std::endl; 
    std::cout << v << std::endl;


    // std::cout << 1.0 - test.M4().norm() << std::endl;
    // std::cout << 1.0 - test.M6().norm() << std::endl;
    return 0;

}