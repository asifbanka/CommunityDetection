#!/usr/bin/env zsh

./plotter.py -f "$(ls benchmarkoutput/nonoverlap_noniter/1000*small*)"     -m nonoverlap -i 0 -o plots/nonoverlap_noniter_1000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/nonoverlap_noniter/5000*small*)"     -m nonoverlap -i 0 -o plots/nonoverlap_noniter_5000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/nonoverlap_noniter/1000*big*)"       -m nonoverlap -i 0 -o plots/nonoverlap_noniter_1000_big.pdf
./plotter.py -f "$(ls benchmarkoutput/nonoverlap_noniter/5000*big*)"       -m nonoverlap -i 0 -o plots/nonoverlap_noniter_5000_big.pdf

./plotter.py -f "$(ls benchmarkoutput/nonoverlap_iter/1000*small*)"        -m nonoverlap -i 9 -o plots/nonoverlap_iter_1000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/nonoverlap_iter/5000*small*)"        -m nonoverlap -i 9 -o plots/nonoverlap_iter_5000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/nonoverlap_iter/1000*big*)"          -m nonoverlap -i 9 -o plots/nonoverlap_iter_1000_big.pdf
./plotter.py -f "$(ls benchmarkoutput/nonoverlap_iter/5000*big*)"          -m nonoverlap -i 9 -o plots/nonoverlap_iter_5000_big.pdf

./plotter.py -f "$(ls benchmarkoutput/overlap_noniter/1000*small*0.1mu*)"  -m overlap    -i 0 -o plots/overlap_noniter_0.1mu_1000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_noniter/5000*small*0.1mu*)"  -m overlap    -i 0 -o plots/overlap_noniter_0.1mu_5000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_noniter/1000*big*0.1mu*)"    -m overlap    -i 0 -o plots/overlap_noniter_0.1mu_1000_big.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_noniter/5000*big*0.1mu*)"    -m overlap    -i 0 -o plots/overlap_noniter_0.1mu_5000_big.pdf

./plotter.py -f "$(ls benchmarkoutput/overlap_noniter/1000*small*0.3mu*)"  -m overlap    -i 0 -o plots/overlap_noniter_0.3mu_1000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_noniter/5000*small*0.3mu*)"  -m overlap    -i 0 -o plots/overlap_noniter_0.3mu_5000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_noniter/1000*big*0.3mu*)"    -m overlap    -i 0 -o plots/overlap_noniter_0.3mu_1000_big.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_noniter/5000*big*0.3mu*)"    -m overlap    -i 0 -o plots/overlap_noniter_0.3mu_5000_big.pdf

./plotter.py -f "$(ls benchmarkoutput/overlap_iter/1000*small*0.1mu*)"     -m overlap    -i 9 -o plots/overlap_iter_0.1mu_1000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_iter/5000*small*0.1mu*)"     -m overlap    -i 9 -o plots/overlap_iter_0.1mu_5000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_iter/1000*big*0.1mu*)"       -m overlap    -i 9 -o plots/overlap_iter_0.1mu_1000_big.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_iter/5000*big*0.1mu*)"       -m overlap    -i 9 -o plots/overlap_iter_0.1mu_5000_big.pdf

./plotter.py -f "$(ls benchmarkoutput/overlap_iter/1000*small*0.3mu*)"     -m overlap    -i 9 -o plots/overlap_iter_0.3mu_1000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_iter/5000*small*0.3mu*)"     -m overlap    -i 9 -o plots/overlap_iter_0.3mu_5000_small.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_iter/1000*big*0.3mu*)"       -m overlap    -i 9 -o plots/overlap_iter_0.3mu_1000_big.pdf
./plotter.py -f "$(ls benchmarkoutput/overlap_iter/5000*big*0.3mu*)"       -m overlap    -i 9 -o plots/overlap_iter_0.3mu_5000_big.pdf
