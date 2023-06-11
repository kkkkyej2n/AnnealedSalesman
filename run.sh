#!/bin/sh
# Run all annealing simulations
# ./run.sh <show>
# If show=0, don't show plots

show=1
if [ $# == 1 ]; then
    show=$1
fi

if [ ${show} == 1 ]; then
    ./annealed_salesman.py 20cities.dat 1000 200000
else
    ./annealed_salesman.py 20cities.dat 1000 200000 ${show} > cities.out
fi

