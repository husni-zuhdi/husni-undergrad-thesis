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

# Run Simulation 6 7 8
# for i in  7 8 9 10
# do
#   cd ~/iter-tritium-breeding-xgboost/jupyter-notebooks/1-calculate-tbr
#   enr=$(python -c "print(round(((0.2*$i)-(1.1)), 2))")
#   mkdir "calculate_tbr/$i-$enr-0.1-100-1000"
#   cp calculate_tbr.py "calculate_tbr/$i-$enr-0.1-100-1000/calculate_tbr.py"
#   cd "calculate_tbr/$i-$enr-0.1-100-1000"
#   python calculate_tbr.py --enrich_Li $enr --neutron_multi 0.1 --batch 100 --part_batch 1000
# done

# Run Base Simulation with fixed code
#  for i in 0.1 0.3 0.5 0.7 0.9
#for i in 0.5 0.7 0.9
# do
#  cd ~/iter-tritium-breeding-xgboost/jupyter-notebooks/1-calculate-tbr
#  mkdir "calculate_tbr/$i-0-0-100-1000"
#  cp calculate_tbr.py "calculate_tbr/$i-0-0-100-1000/calculate_tbr.py"
#  cd "calculate_tbr/$i-0-0-100-1000"
#  python calculate_tbr.py --enrich_Li $i --mod_ratio 0  --neutron_multi 0 --batch 100 --part_batch 1000
#done

# Run 0.1 mod_ratio 0 neutron_multiplier simulation with fixed code
for i in 0.1 0.3 0.5 0.7 0.9
do
  cd ~/iter-tritium-breeding-xgboost/jupyter-notebooks/1-calculate-tbr
  mkdir  "calculate_tbr/$i-0.1-0-100-1000"
  cp calculate_tbr.py "calculate_tbr/$i-0.1-0-100-1000/calculate_tbr.py"
  cd "calculate_tbr/$i-0.1-0-100-1000"
  python calculate_tbr.py --enrich_Li $i --mod_ratio 0.1 --neutron_multi 0 --batch 100  --part_batch 1000
done
