#include <cmath>
#include <complex>
#include <functional>
#include <iostream>
#include <vector>
#include <string>
#include <chrono>

#include <Eigen/Dense>

using std::complex;
using std::vector;
using namespace std::complex_literals;
using std::function;
using std::string;

using Eigen::Matrix;

class Methods;

double f_prof(double t, double v0, double n)
{
    return v0 * exp(-n * t);
}

class Methods
{
public:
    Matrix<double, 3, 3> H0;
    Matrix<double, 3, 3> W;

    Methods(
        Matrix<double, 3, 3> H0,
        Matrix<double, 3, 3> W,
        Matrix<complex<double>, 3, 1> v,
        function<double(double)> prof,
        double start,
        double end,
        double steps,
        double e
    ): H0(H0), W(W), v(v), start(start), end(end), prof(prof), e(e)
    {
        if (steps >= 1) this->step = (end - start) / (steps);
        else this->step = steps;
    }

    Matrix<complex<double>, 3, 1> M2()
    {
        Matrix<complex<double>, 3, 3> A;
        auto Y = v;
        auto point = start; 
        while (point < end)
        {

            A = -step * (H0 + prof(point + step / 2.0) * W);
            Y = matrix_exp_puzzer(A, Y, -1.0);

            #ifdef DEBUG_LINTERNALS
                std::cout << "--------------------" << t << "-------------------" << std::endl;
                print_more_info(Y, *this);
            #endif
            point += step;
        }
        return Y;
    }

    Matrix<complex<double>, 3, 1> M4()
    {
        auto Y = v;
        double c1 = 0.5 - sqrt(3.0) / 6.0;
        double c2 = 0.5 + sqrt(3.0) / 6.0;
        Matrix<complex<double>, 3, 3> A1;
        Matrix<complex<double>, 3, 3> A2;
        Matrix<complex<double>, 3, 3> omega;
        auto point = start; 
        while (point < end)
        {
            A1 = H0 + prof(point + c1 * step) * W;
            A2 = H0 + prof(point + c2 * step) * W;
            omega = (-step / 2.0) * (A1 + A2) + 1i * (sqrt(3.0) / 12.0 * step * step) * (A2*A1-A1*A2);
            Y = matrix_exp_puzzer(omega, Y, 1.0);

            #ifdef DEBUG_LINTERNALS
                std::cout << "--------------------" << t << "-------------------" << std::endl;
                print_more_info(Y, *this);
            #endif
            point += step;
        }

        return Y;
    }

    Matrix<complex<double>, 3, 1> M6()
    {
        auto Y = v;
        double c1 = 0.5 - sqrt(15.0) / 10.0;
        double c2 = 0.5;
        double c3 = 0.5 + sqrt(15.0) / 10.0;

        Matrix<complex<double>, 3, 3> A1;
        Matrix<complex<double>, 3, 3> A2;
        Matrix<complex<double>, 3, 3> A3;

        Matrix<complex<double>, 3, 3> B1, B2, B3;

        Matrix<complex<double>, 3, 3> T1, T2, T3, T4;

        Matrix<complex<double>, 3, 3> omega;

        auto point = start;
        while (point < end)
        {
            A1 = H0 + prof(point + c1 * step) * W;
            A2 = H0 + prof(point + c2 * step) * W;
            A3 = H0 + prof(point + c3 * step) * W;

            B1 = step * A2;
            B2 = (sqrt(15.0) * step / 3.0) * (A3 - A1);
            B3 = (10.0 * step / 3.0) * (A3 - 2.0 * A2 + A1);

            T1 = B2 * B1 - B1 * B2;
            T2 = 2.0 * B3 + 1i * T1;
            T3 = T2 * B1 - B1 * T2;
            T4 = B2 - 1i / 60.0 * T3;

            T2 = -20.0 * B1 - B3 + 1i * T1;
            T1 = 1i / 240.0 * (T4 * T2 - T2 * T4);

            omega = -1.0 * (B1 + 0.5 * B3 + T1);
            Y = matrix_exp_puzzer(omega, Y, 1.0);

            // more info
            #ifdef DEBUG_LINTERNALS
                std::cout << "--------------------" << t << "-------------------" << std::endl;
                print_more_info(Y, *this);
            #endif
            point += step;
        }
        return Y;
    }

    Matrix<complex<double>, 3, 1> CF4()
    {
        double c1 = 0.5 - sqrt(3.0)/6.0;
        double c2 = 0.5 + sqrt(3.0)/6.0;
        
        double a1 = 0.25 - sqrt(3.0)/6.0;
        double a2 = 0.25 + sqrt(3.0)/6.0;
        
        Matrix<complex<double>, 3, 3> A1, A2;
        Matrix<complex<double>, 3, 3> omega;
        auto Y = v;
        auto point = start;
        while (point < end)
        {
            A1 = H0 + prof(point + c1 * step) * W;
            A2 = H0 + prof(point + c2 * step) * W;

            omega = -step*(a2*A1 + a1*A2);
            Y = matrix_exp_puzzer(omega, Y, 1.0);

            omega = -step*(a1*A1 + a2*A2);
            Y = matrix_exp_puzzer(omega, Y, 1.0);

            #ifdef DEBUG_LINTERNALS
                std::cout << "--------------------" << t << "-------------------" << std::endl;
                print_more_info(Y, *this);
            #endif
            point += step;
        }
        return Y;
    }

    Matrix<complex<double>, 3, 1> CF4_3()
    {
        double c1 = 0.5 - sqrt(15.0) / 10.0;
        double c2 = 0.5;
        double c3 = 0.5 + sqrt(15.0) / 10.0;

        double a11 = 37.0/240.0 - 10.0*sqrt(15.0)/261.0;
        double a12 = -1.0/30.0;
        double a13 = 37.0/240.0 + 10.0*sqrt(15.0)/261.0;
        double a21 = -11.0/360.0;
        double a22 = 23.0/45.0;
        double a23 = -11.0/360.0;
        double a31 = 37.0/240.0 + 10.0*sqrt(15.0)/261.0;
        double a32 = -1.0/30.0;
        double a33 = 37.0/240.0 - 10.0*sqrt(15.0)/261.0;

        Matrix<complex<double>, 3, 3> A1, A2, A3, Y1, Y2, Y3;
        auto Y = v;
        auto point = start;
        while (point < end)
        {
            A1 = H0 + prof(point + c1 * step) * W;
            A2 = H0 + prof(point + c2 * step) * W;
            A3 = H0 + prof(point + c3 * step) * W;

            Y1 = -step*(a11*A1 + a12*A2 + a13*A3);
            Y2 = -step*(a21*A1 + a22*A2 + a23*A3);
            Y3 = -step*(a31*A1 + a32*A2 + a33*A3);

            Y = matrix_exp_puzzer(Y3, Y, 1.0);
            Y = matrix_exp_puzzer(Y2, Y, 1.0);
            Y = matrix_exp_puzzer(Y1, Y, 1.0);


            #ifdef DEBUG_LINTERNALS
                std::cout << "--------------------" << t << "-------------------" << std::endl;
                print_more_info(Y, *this);
            #endif
            point += step;
        }
        return Y;
    }

    void print_more_info(Matrix<complex<double>, 3, 1>& v)
    {
        std::cout.precision(14);
        std::cout << "p = " << p << " q = " << q << std::endl;
        std::cout << "lb0 = " << lbd0 << " lbd1 = " << lbd1 << " lbd2 = " << lbd2 << std::endl;
        std::cout << "e = " << e << std::endl;
        std::cout << v << std::endl;
        std::cout << "1-norm " << 1.0 - v.norm() << std::endl;
        std::cout << "norm0 = " << std::abs(v(0,0)) << std::endl;
        std::cout << "norm1 = " << std::abs(v(1,0)) << std::endl;
        std::cout << "norm2 = " << std::abs(v(2,0)) << std::endl;
        std::cout << "arg0 = " << std::arg(v(0, 0)) << std::endl;
        std::cout << "arg1 = " << std::arg(v(1, 0)) << std::endl;
        std::cout << "arg2 = " << std::arg(v(2, 0)) << std::endl;
    }

private:
    Matrix<complex<double>, 3, 1> v;
    double start;
    double end;
    double step;
    complex<double> p;
    complex<double> q;
    complex<double> lbd0;
    complex<double> lbd1;
    complex<double> lbd2;
    complex<double> a;
    complex<double> b;
    complex<double> c;
    complex<double> r0;
    complex<double> r1;
    function<double(double)> prof;
    double e;

    complex<double> calc_lambda(double k, complex<double> p, complex<double> q)
    {
        return cos((1.0 / 3.0) * acos((3.0 * q / (2.0 * p)) * sqrt(3.0 / p)) - 2.0 * M_PI * k / 3.0);
    }

    Matrix<complex<double>, 3, 1> matrix_exp_puzzer(
        Matrix<complex<double>, 3, 3>& matrix,
        Matrix<complex<double>, 3, 1>& vectr,
        double t)
    {
        Matrix<double, 3, 3> I;
        I << 1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0;
        complex<double> z = matrix.trace() / 3.0;
        Matrix<complex<double>, 3, 3> matrix0 = matrix - z * I;

        p = (matrix0 * matrix0).trace() * 0.5;
        q = matrix0.determinant();

        lbd0 = calc_lambda(0.0, p, q);
        lbd1 = calc_lambda(1.0, p, q);
        lbd2 = calc_lambda(2.0, p, q);

        a = lbd1 - lbd0;
        b = lbd2 - lbd0;
        c = lbd1 - lbd2;

        lbd0 *= 2.0 * sqrt(p / 3.0);
        lbd1 *= 2.0 * sqrt(p / 3.0);
        lbd2 *= 2.0 * sqrt(p / 3.0);
        a *= 2.0 * sqrt(p / 3.0);
        b *= 2.0 * sqrt(p / 3.0);
        c *= 2.0 * sqrt(p / 3.0);

        r0 = -1.0 * (2.0 * sin(a / 2.) * sin(a / 2.) - 1i * sin(a)) / a;
        r1 = -1.0 / c * (-r0 - (2.0 * sin(b / 2.0) * sin(b / 2.0) - 1i * sin(b)) / b);

        Matrix<complex<double>, 3, 1> q1 = (1.0 - lbd0 * (r0 - lbd1 * r1)) * vectr;
        Matrix<complex<double>, 3, 1> psi = matrix0 * vectr;
        Matrix<complex<double>, 3, 1> q2 = (r0 + lbd2 * r1) * psi;
        Matrix<complex<double>, 3, 1> q3 = r1 * matrix0 * psi;

        return exp(1i * t * z) * exp(1i * lbd0 * t) * (q1 + q2 + q3);
    }
};

int main(int argc, char *argv[])
{
    if (argc != 6)
    {
        return 1;
    }
    double start = std::stod(argv[1]);
    double end = std::stod(argv[2]);
    double steps = std::stod(argv[3]);
    string mthd = argv[4];
    double e = std::stod(argv[5]);


    Matrix<std::complex<double>, 3, 1> v1;
    v1(0, 0) = 1.0;

    // ----- H0 -----
    Matrix<double, 3, 3> H0;
    H0.setZero();
    double a = 4.35196e6 / e;
    double b = 0.030554;
    H0(1, 1) = a * b;
    H0(2, 2) = a;

    // ----- W -----
    double s12 = std::sqrt(0.308);
    // double s23 = std::sqrt(0.437);
    double s13 = std::sqrt(0.0234);
    double c12 = std::sqrt(1.0 - std::pow(s12, 2));
    // double c23 = std::sqrt(1 - std::pow(s23, 2));
    double c13 = std::sqrt(1.0 - std::pow(s13, 2));

    Eigen::Matrix<double, 3, 3> W;
    W << c13 * c13 * c12 * c12, c12 * s12 * c13 * c13, c12 * c13 * s13,
        c12 * s12 * c13 * c13, s12 * s12 * c13 * c13, s12 * c13 * s13,
        c12 * c13 * s13, s12 * c13 * s13, s13 * s13;

    // ----- other -----
    double v0 = 6.5956e4;
    double n = 10.54;
    function<double(double)> prof = [=](double t) { return f_prof(t, v0, n) ; };

    std::cout.precision(14);

    Methods test = Methods(H0, W, v1, prof, start, end, steps, e);
    std::cout << "H0 = " << H0 << std::endl;
    std::cout << "W = " << W << std::endl;
    std::cout << "v = " << v1 << std::endl;
    std::cout << "start = " << start << " end = " << end << " step = " << steps << std::endl;

    Matrix<std::complex<double>, 3, 1> v;

    

    auto start_time = std::chrono::high_resolution_clock::now();

    if (mthd == "M2") v = test.M2();
    if (mthd == "M4") v = test.M4();
    if (mthd == "M6") v = test.M6();
    if (mthd == "CF4") v = test.CF4();
    if (mthd == "CF4:3") v = test.CF4_3();

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> time = (end_time - start_time);

    std::cout << "------------------ final ---------------------" << std::endl;
    test.print_more_info(v);
    std::cout<<"P = "<<std::defaultfloat<<( c12*c12*c13*c13*abs(v(0))*abs(v(0))+
                      s12*s12*c13*c13*abs(v(1))*abs(v(1))+
                      s13*s13*abs(v(2))*abs(v(2)) ) << std::endl;

    
    std::cout << "time = " << time.count() << std::endl;

    return 0;
}
