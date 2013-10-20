set encoding utf8
set xlabel "Rank"
set ylabel "Frequency"
set grid

## liczba słów
b = 160

## plik z danymi: rank frequency
FILE = 'gsm.freq'

## katalog z obrazkami



set xrange [1:b]

f1(x) = a/x
fit f1(x) FILE using 0:1 via a

set terminal png size 1000,600 enhanced font 'Verdana,10'

set output 'z03_zipf.png'
plot FILE with points lt 2 lw 1 lc rgb "#000000" notitle,\
0 <= x && x <= b ? f1(x) : 1/0 notitle

set output 'z03_zipf-log.png'
set logscale xy
plot FILE with points lt 2 lw 1 lc rgb "#000000" notitle,\
0 <= x && x <= b ? f1(x) : 1/0 notitle
set nologscale xy 

f2(x) = P/((x+d)**B)
P = 10000
#d = 1
#B=0.00001
fit f2(x) FILE using 0:1 via P, d, B

set output 'z03_mandelbrot.png'
plot FILE with points lt 2 lw 1 lc rgb "#000000" notitle,\
0 <= x && x <= b ? f2(x) : 1/0 notitle

set output 'z03_mandelbrot-log.png'
set logscale xy
plot FILE with points lt 2 lw 1 lc rgb "#000000" notitle,\
0 <= x && x <= b ? f2(x) : 1/0 notitle
set nologscale xy 
