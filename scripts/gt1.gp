#!/usr/bin/env gnuplot

set term pdfcairo enhanced font "Consolas,12"
set logscale x
set logscale y

gt_s = "gt1"
inData(a,b) = sprintf("%s_(%s,%s).dat", gt_s, a, b)
outF(a) = sprintf("%s_%s.pdf", gt_s, a)

set title "Absolute execution time"

rg = inData('0.1', '0.15')
set output outF("rg1")

plot rg u 1:2 w lp t 'M2', '' u 1:4 w lp t 'M4', '' u 1:6 w lp t 'M6', \
  '' u 1:8 w lp t 'CF4', '' u 1:10 w lp t 'CF4:3'

rg = inData('0.1', '0.2')
set output outF("rg2")

plot rg u 1:2 w lp t 'M2', '' u 1:4 w lp t 'M4', '' u 1:6 w lp t 'M6', \
  '' u 1:8 w lp t 'CF4', '' u 1:10 w lp t 'CF4:3'

rg = inData('0.1', '0.3')
set output outF("rg3")

plot rg u 1:2 w lp t 'M2', '' u 1:4 w lp t 'M4', '' u 1:6 w lp t 'M6', \
  '' u 1:8 w lp t 'CF4', '' u 1:10 w lp t 'CF4:3'
