set term pdfcairo
set output "graf.pdf"
set xrange [0.00000000001:1]
set logscale x 10
set yrange [-0.05:0.1]
plot "for_gnuplot_M2.dat" t "M2", "for_gnuplot_M4.dat" t "M4", "for_gnuplot_M6.dat" t "M6", "for_gnuplot_Cf4.dat" t "Cf4", "for_gnuplot_Cf4_3.dat" t "Cf4_3"

set output "graf_detail.pdf"
set logscale y 10
set yrange [1e-6 : 0.1]
plot "for_gnuplot_M2.dat" t "M2", "for_gnuplot_M4.dat" t "M4", "for_gnuplot_M6.dat" t "M6", "for_gnuplot_Cf4.dat" t "Cf4", "for_gnuplot_Cf4_3.dat" t "Cf4_3" pt 6