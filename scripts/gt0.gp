#!/usr/bin/env gnuplot

set term pdfcairo enhanced font "Consolas,12"
set logscale x
set logscale y

fileName(a,b) = sprintf("gt0_(%s,%s).dat", a,b)

rg=fileName('0.1', '0.15')
set output "gt0_rg1.pdf"
plot rg u 1:2 w lp t 'M2', '' u 1:4 w lp t 'M4', '' u 1:6 w lp t 'M6', \
  '' u 1:8 w lp t 'CF4', '' u 1:10 w lp t 'CF4:3'

rg=fileName('0.1', '0.2')
set output "gt0_rg2.pdf"
plot rg u 1:2 w lp t 'M2', '' u 1:4 w lp t 'M4', '' u 1:6 w lp t 'M6', \
  '' u 1:8 w lp t 'CF4', '' u 1:10 w lp t 'CF4:3'

rg=fileName('0.1', '0.3')
set output "gt0_rg3.pdf"
plot rg u 1:2 w lp t 'M2', '' u 1:4 w lp t 'M4', '' u 1:6 w lp t 'M6', \
  '' u 1:8 w lp t 'CF4', '' u 1:10 w lp t 'CF4:3'
