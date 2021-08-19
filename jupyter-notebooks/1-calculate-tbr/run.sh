#!/bin/bash

# Change mod and nm number
export mod=0
export nm=0
for i in 0.1 0.3 0.5 0.7 0.9
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
  gsutil cp results.json gs://iter-tritium-breeding-xgboost-bucket/results/$i-$mod-$nm-100-1000.json
  gsutil cp statepoint.100.h5 gs://iter-tritium-breeding-xgboost-bucket/statepoint/$i-$mod-$nm-100-1000.h5
  gsutil cp tallies.out gs://iter-tritium-breeding-xgboost-bucket/tallies/$i-$mod-$nm-100-1000.out
  gsutil cp n-Xt_on_3D_mesh.vtk gs://iter-tritium-breeding-xgboost-bucket/3D-mesh/$i-$mod-$nm-100-1000.vtk
  gsutil cp n-Xt_on_2D_mesh_xy.png gs://iter-tritium-breeding-xgboost-bucket/2D-mesh/xy/$i-$mod-$nm-100-1000.png
  gsutil cp n-Xt_on_2D_mesh_xz.png gs://iter-tritium-breeding-xgboost-bucket/2D-mesh/xz/$i-$mod-$nm-100-1000.png
  gsutil cp n-Xt_on_2D_mesh_yz.png gs://iter-tritium-breeding-xgboost-bucket/2D-mesh/yz/$i-$mod-$nm-100-1000.png
done
# Next mod=0.1 nm=0
