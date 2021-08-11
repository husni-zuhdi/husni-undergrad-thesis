#!/bin/bash

# Run Simulation 1 2
# cd 1-0.1-0-100-1000/
# python calculate_tbr.py --enrich_Li 0.1 --neutron_multi 0 --batch 100 --part_batch 1000
# cd ../2-0.3-0-100-1000/
# python calculate_tbr.py --enrich_Li 0.3 --neutron_multi 0 --batch 100 --part_batch 1000

# Run Simulation 3 4 5
# for i in 3 4 5
# do
#  cd ~/iter-tritium-breeding-xgboost/jupyter-notebooks/1-calculate-tbr
#  enr=$(python -c "print(round(((0.2*$i)-(0.1)), 2))")
#  mkdir "calculate_tbr/$i-$enr-0-100-1000"
#  cp calculate_tbr.py "calculate_tbr/$i-$enr-0-100-1000/calculate_tbr.py"
#  cd "calculate_tbr/$i-$enr-0-100-1000"
#  python calculate_tbr.py --enrich_Li $enr --neutron_multi 0 --batch 100 --part_batch 1000
#done

# Standard Deviations Summation
# https://stats.stackexchange.com/questions/25848/how-to-sum-a-standard-deviation
