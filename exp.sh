#!/bin/sh
# This is for running experiments on the cloud
set -x
expName="CPUvsGPU"
if [ $1 == 'cpu' ]
then
    for seed in {1..100}
    do
        sbatch -J $expName ~/bin/bluemoon.sh ds2 python 3.minLA_cpu.py --seed=$seed --exp_name=$expName --tag=$1
    done
fi

if [ $1 == 'gpu' ]
then
    for seed in {1..100}
    do
        sbatch -J $expName ~/bin/deepgreen.sh ds2 python 4.minLA_gpu.py --seed=$seed --exp_name=$expName --tag=$1
    done
fi
