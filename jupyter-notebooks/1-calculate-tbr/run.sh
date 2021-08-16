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
#for i in 0.1 0.3 0.5 0.7 0.9
#do
#  cd ~/iter-tritium-breeding-xgboost/jupyter-notebooks/1-calculate-tbr
#  mkdir  "calculate_tbr/$i-0.1-0-100-1000"
#  cp calculate_tbr.py "calculate_tbr/$i-0.1-0-100-1000/calculate_tbr.py"
#  cd "calculate_tbr/$i-0.1-0-100-1000"
#  echo "Start simulating $i Li-6 enrichment + 0.1 Mod Ratio + 0 Neutron Multiplier Ratio"
#  python calculate_tbr.py --enrich_Li $i --mod_ratio 0.1 \
#  --neutron_multi 0 --batch 100  --part_batch 1000
#
#  # If you want to save your simulation result in a bucket (I use google cloud storage her)
#  # make sure to change the name of bucket. If not, comment the code bellow
#  gsutil cp results.json gs://iter-tritium-breeding-xgboost-bucket/results/$i-0.1-0.3-100-1000.json
#done

# Run 0.1 mod_ratio 0.1 neutron_multiplier simulation with fixed code
#for i in 0.1 0.3 0.5 0.7 0.9
#do
#  cd ~/iter-tritium-breeding-xgboost/jupyter-notebooks/1-calculate-tbr
#  mkdir  "calculate_tbr/$i-0.1-0.1-100-1000"
#  cp calculate_tbr.py "calculate_tbr/$i-0.1-0.1-100-1000/calculate_tbr.py"
#  cd "calculate_tbr/$i-0.1-0.1-100-1000"
#  python calculate_tbr.py --enrich_Li $i --mod_ratio 0.1 \
#  --neutron_multi 0.1 --batch 100 --part_batch 1000
#done

# Run 0.1 mod_ratio 0.3 neutron_multiplier simulation with fixed code
# for i in 0.1 0.3
export mod=0.1
export nm=0.3
for i in 0.5 0.7 0.9
do
  cd ~/iter-tritium-breeding-xgboost/jupyter-notebooks/1-calculate-tbr
  mkdir  "calculate_tbr/$i-$mod-$nm-100-1000"
  cp calculate_tbr.py "calculate_tbr/$i-$mod-$nm-100-1000/calculate_tbr.py"
  cd "calculate_tbr/$i-$mod-$nm-100-1000"
  echo "Start simulating $i Li-6 enrichment + $mod Mod Ratio + $nm Neutron Multiplier Ratio"
  python calculate_tbr.py --enrich_Li $i --mod_ratio $mod \
  --neutron_multi $nm --batch 100 --part_batch 1000
  
  # If you want to save your simulation result in a bucket (I use google cloud storage her)
  # make sure to change the name of bucket. If not, comment the code bellow
  gsutil cp results.json gs://iter-tritium-breeding-xgboost-bucket/results/$i-$mod-$nm-100-1000.json'
  gsutil cp statepoint.100.h5 gs://iter-tritium-breeding-xgboost-bucket/statepoint/$i-0.1-0.3-100-1000.h5
  gsutil cp tallies.out gs://iter-tritium-breeding-xgboost-bucket/tallies/$i-0.1-0.3-100-1000.out
  gsutil cp n-Xt_on_3D_mesh.vtk gs://iter-tritium-breeding-xgboost-bucket/3D-mesh/$i-0.1-0.3-100-1000.vtk
  gsutil cp n-Xt_on_2D_mesh_xy.png gs://iter-tritium-breeding-xgboost-bucket/2D-mesh/xy/$i-0.1-0.3-100-1000.png
  gsutil cp n-Xt_on_2D_mesh_xz.png gs://iter-tritium-breeding-xgboost-bucket/2D-mesh/xz/$i-0.1-0.3-100-1000.png
  gsutil cp n-Xt_on_2D_mesh_yz.png gs://iter-tritium-breeding-xgboost-bucket/2D-mesh/yz/$i-0.1-0.3-100-1000.png
done
