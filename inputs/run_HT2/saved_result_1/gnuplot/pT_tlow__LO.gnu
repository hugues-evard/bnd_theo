

reset
set terminal pdfcairo enhanced dashed dl 1.5 lw 3 font "Helvetica,30" size 7.6, 8
#set terminal pdfcairo enhanced dashed dl 1.5 lw 4 font "Helvetica,30" size 7.6, 7.4
set encoding utf8
## default key features
#set key at graph 1.03,0.97
set key reverse  # put text on right side
set key Left     # left bounded text
set key spacing 1.1
set key samplen 2
## to have a assisting grid of dashed lines
set grid front
## set margins
set lmargin 5
set rmargin 2

## general settings
set key at graph 0.93, 0.95
set xtics 
set mxtics 
set mytics 10
set logscale y
#set logscale x
set ytic offset 0, 0.1
set format y "10^{\%T}"

#set label front "MATRIX (arXiv:1711.06631)" font "Courier,26" rotate by 90 at graph 1.02, graph 0.01
#set label front "MATRIX ({/Courier=20 arXiv:1711.06631using OpenLoops})" font "Courier,26" rotate by 90 at graph 1.02, graph -0.51
set label front "produced with MATRIX {/Courier=22(using OpenLoops)}" font "Courier,26" rotate by 270 at graph 1.03, graph 1.0
#, arXiv:1711.06631
set label "{/Symbol s} [fb]" at graph 0, 1.06
set label "p p --> top anti-top\\@LHC 13.0 TeV" right at graph 1, graph 1.07

set output "/ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/pT_tlow__LO.pdf"

##############
# main frame #
##############

# origin, size of main frame
set origin 0, 0.4
set size 1, 0.53
set bmargin 0 # set marging to remove space
set tmargin 0 # set margin to remove space
set format x ""

## define line styles
set style line 2 dt (3,3) lc rgb "black" lw 1
set style line 3 dt (7,4) lc rgb "red" lw 1.25
set style line 1 lt 1 lc rgb "blue" lw 0.75
set style line 4 dt (10,3,3,3) lc rgb "forest-green" lw 0.75
set style line 5 lt 5 lc rgb "orange" lw 0.75
set style line 6 lt 6 lc rgb "magenta" lw 0.75
## for the uncertainty band borders (less thick)
set style line 12 dt (3,3) lc rgb "black" lw 0.1
set style line 13 dt (9,6) lc rgb "red" lw 0.1
set style line 11 lt 1 lc rgb "blue" lw 0.1
set style line 14 dt (10,3,3,3) lc rgb "forest-green" lw 0.1
set style line 15 lt 5 lc rgb "orange" lw 0.1
set style line 16 lt 6 lc rgb "magenta" lw 0.1 

## define ranges
set xrange [0.0:800.0]
set yrange [:]

set multiplot
plot "/ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist" using 1:3 with lines ls 1 title "LO_{QCD}", "/ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist" using 1:5:7 with filledcurves ls 1 fs transparent solid 0.15 notitle, "/ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist" using 1:5 with lines ls 11 notitle, "/ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist" using 1:7 with lines ls 11 notitle
###############
# ratio inset #
###############

## remove previous settings
unset label  
#unset key
unset logscale y
unset format

## set ratio inset size
set size 1, 0.23
set origin 0, 0.12

## can be changed
#set logscale y
#set logscale x
set format y 
set key at graph 0.93, 0.95
set label "ratio to LO_{QCD}" at graph 0, 1.1
set yrange [4.8153076923076924e-08:1.0]
#set ytics 0.2
#set mytics 2.0
set ytic offset 0.4, 0
set xtic offset -0.21,0.4
set xtics 
set mxtics 
set xlabel offset 0,0.7
set xlabel  "pT_tlow__LO "
plot "<paste /ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist /ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist" using 1:($3/$13) with lines ls 1 notitle, "<paste /ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist /ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist" using 1:($5/$12):($7/$12) with filledcurves ls 1 fs transparent solid 0.15 notitle, "<paste /ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist /ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist" using 1:($5/$12) with lines ls 11 notitle, "<paste /ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist /ada_mnt/ada/user/hevard/matrix/MATRIX_v2.1.0/run/ppttx20_MATRIX/result/run_HT2/gnuplot/histograms/pT_tlow__LO.hist" using 1:($7/$12) with lines ls 11 notitle