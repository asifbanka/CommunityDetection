#!/usr/bin/env bash

# transforms json files to pdfs
# call like this:
# makeallplots.sh path/to/json/files /outputfolder/for/pdfs

DIR=${0%/*}
plotter=$DIR/plotter.py

indir=$1
outdir=$2

iterations=9

$plotter -f "$(ls $indir/nonoverlap_noniter/1000*small*)"     -m nonoverlap -i 0           -o $outdir/nonoverlap_noniter_a.pdf
$plotter -f "$(ls $indir/nonoverlap_noniter/1000*big*)"       -m nonoverlap -i 0           -o $outdir/nonoverlap_noniter_b.pdf
$plotter -f "$(ls $indir/nonoverlap_noniter/5000*small*)"     -m nonoverlap -i 0           -o $outdir/nonoverlap_noniter_c.pdf
$plotter -f "$(ls $indir/nonoverlap_noniter/5000*big*)"       -m nonoverlap -i 0           -o $outdir/nonoverlap_noniter_d.pdf

$plotter -f "$(ls $indir/nonoverlap_iter/1000*small*)"        -m nonoverlap -i $iterations -o $outdir/nonoverlap_iter_a.pdf
$plotter -f "$(ls $indir/nonoverlap_iter/1000*big*)"          -m nonoverlap -i $iterations -o $outdir/nonoverlap_iter_b.pdf
$plotter -f "$(ls $indir/nonoverlap_iter/5000*small*)"        -m nonoverlap -i $iterations -o $outdir/nonoverlap_iter_c.pdf
$plotter -f "$(ls $indir/nonoverlap_iter/5000*big*)"          -m nonoverlap -i $iterations -o $outdir/nonoverlap_iter_d.pdf

$plotter -f "$(ls $indir/overlap_noniter/1000*small*0.1mu*)"  -m overlap    -i 0           -o $outdir/overlap_noniter_1mu_a.pdf
$plotter -f "$(ls $indir/overlap_noniter/1000*big*0.1mu*)"    -m overlap    -i 0           -o $outdir/overlap_noniter_1mu_b.pdf
$plotter -f "$(ls $indir/overlap_noniter/5000*small*0.1mu*)"  -m overlap    -i 0           -o $outdir/overlap_noniter_1mu_c.pdf
$plotter -f "$(ls $indir/overlap_noniter/5000*big*0.1mu*)"    -m overlap    -i 0           -o $outdir/overlap_noniter_1mu_d.pdf

$plotter -f "$(ls $indir/overlap_noniter/1000*small*0.3mu*)"  -m overlap    -i 0           -o $outdir/overlap_noniter_3mu_a.pdf
$plotter -f "$(ls $indir/overlap_noniter/1000*big*0.3mu*)"    -m overlap    -i 0           -o $outdir/overlap_noniter_3mu_b.pdf
$plotter -f "$(ls $indir/overlap_noniter/5000*small*0.3mu*)"  -m overlap    -i 0           -o $outdir/overlap_noniter_3mu_c.pdf
$plotter -f "$(ls $indir/overlap_noniter/5000*big*0.3mu*)"    -m overlap    -i 0           -o $outdir/overlap_noniter_3mu_d.pdf

$plotter -f "$(ls $indir/overlap_iter/1000*small*0.1mu*)"     -m overlap    -i $iterations -o $outdir/overlap_iter_1mu_a.pdf
$plotter -f "$(ls $indir/overlap_iter/1000*big*0.1mu*)"       -m overlap    -i $iterations -o $outdir/overlap_iter_1mu_b.pdf
$plotter -f "$(ls $indir/overlap_iter/5000*small*0.1mu*)"     -m overlap    -i $iterations -o $outdir/overlap_iter_1mu_c.pdf
$plotter -f "$(ls $indir/overlap_iter/5000*big*0.1mu*)"       -m overlap    -i $iterations -o $outdir/overlap_iter_1mu_d.pdf

$plotter -f "$(ls $indir/overlap_iter/1000*small*0.3mu*)"     -m overlap    -i $iterations -o $outdir/overlap_iter_3mu_a.pdf
$plotter -f "$(ls $indir/overlap_iter/1000*big*0.3mu*)"       -m overlap    -i $iterations -o $outdir/overlap_iter_3mu_b.pdf
$plotter -f "$(ls $indir/overlap_iter/5000*small*0.3mu*)"     -m overlap    -i $iterations -o $outdir/overlap_iter_3mu_c.pdf
$plotter -f "$(ls $indir/overlap_iter/5000*big*0.3mu*)"       -m overlap    -i $iterations -o $outdir/overlap_iter_3mu_d.pdf


$plotter -f $indir/nonoverlap_iter/1000N_bigCommunities_0on_0om_0.02seed.json  -m nonoverlap -i "0 $iterations" -o $outdir/nonoverlap_compare_a.pdf
$plotter -f $indir/nonoverlap_iter/5000N_bigCommunities_0on_0om_0.06seed.json  -m nonoverlap -i "0 $iterations" -o $outdir/nonoverlap_compare_b.pdf

$plotter -f $indir/overlap_iter/1000N_smallCommunities_0.1mu_3om_0.04seed.json -m overlap    -i "0 $iterations" -o $outdir/overlap_compare_a.pdf
$plotter -f $indir/overlap_iter/5000N_bigCommunities_0.1mu_3om_0.06seed.json   -m overlap    -i "0 $iterations" -o $outdir/overlap_compare_b.pdf
