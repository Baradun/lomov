# The repository purpose

This repository contains code to compare different methods for solving
Schoringer-like equation using Magnus expansion. These methods uses fixed step
and Putzer algorithm to compute matrix exponent (for 3×3 matrix).

# How to run the code

The code of main program is written in C++ (actually using some features of
C++2a), most scripts are written in python, for plotting data we use GNUPLOT.

To compile code and run

    meson setup host#$(host_xx=( $(echo $HOSTNAME | sha3-512sum) ) ; xx=${host_xx[0]} ; echo ${xx:0:8})
    cd host#*
    meson compile
    meson compile methods

This requires meson (best with 0.57+), bash, sha3sum (if one uses Ubuntu,
install libdigest-sha3-perl package and use sha3sum -a 512), python3, ncurses
(for methods.py) and pandas (for stat.py).
