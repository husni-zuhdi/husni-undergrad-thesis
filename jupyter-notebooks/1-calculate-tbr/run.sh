#!/bin/bash

# Change mod and nm number
# export mod=0
export mod=0.0
for nm in 0.1 0.3 0.5 0.7
do
  for i in 0.1 0.3 0.5 0.7 0.9
  do
    cd ~/iter-tritium-breeding-xgboost/jupyter-notebooks/1-calculate-tbr
    mkdir  "calculate_tbr/$i-$mod-$nm-20-5000"
    cp calculate_tbr.py "calculate_tbr/$i-$mod-$nm-20-5000/calculate_tbr.py"
    cd "calculate_tbr/$i-$mod-$nm-20-5000"
    echo "======================================================================================"
    echo "Start v3 simulating $i Li-6 enrichment + $mod Mod Ratio + $nm Neutron Multiplier Ratio"
    echo "======================================================================================"
    python calculate_tbr.py --enrich_Li $i --mod_ratio $mod \
    --neutron_multi $nm --batch 20 --part_batch 5000

    # If you want to save your simulation result in a bucket (I use google cloud storage her)
    # make sure to change the name of bucket. If not, comment the code bellow
    gsutil cp results.json gs://iter-tritium-breeding-xgboost-bucket/v3/results/$i-$mod-$nm-20-5000.json
    gsutil cp statepoint.20.h5 gs://iter-tritium-breeding-xgboost-bucket/v3/statepoint/$i-$mod-$nm-20-5000.h5
    gsutil cp tallies.out gs://iter-tritium-breeding-xgboost-bucket/v3/tallies/$i-$mod-$nm-20-5000.out
    gsutil cp n-Xt_on_3D_mesh.vtk gs://iter-tritium-breeding-xgboost-bucket/v3/3D-mesh/$i-$mod-$nm-20-5000.vtk
    gsutil cp n-Xt_on_2D_mesh_xy.png gs://iter-tritium-breeding-xgboost-bucket/v3/2D-mesh/xy/$i-$mod-$nm-20-5000.png
    gsutil cp n-Xt_on_2D_mesh_xz.png gs://iter-tritium-breeding-xgboost-bucket/v3/2D-mesh/xz/$i-$mod-$nm-20-5000.png
    gsutil cp n-Xt_on_2D_mesh_yz.png gs://iter-tritium-breeding-xgboost-bucket/v3/2D-mesh/yz/$i-$mod-$nm-20-5000.png
  done
done
# AWS mod 0.0 nm 0.1 0.3 0.5 0.7
# AWS mod 0.1 nm 0.1 0.3 0.5 0.7
# AWS mod 0.3 nm 0.1 0.3 0.5 0.7
# AWS mod 0.5 nm 0.1 0.3 0.5 0.7
# AWS mod 0.7 nm 0.1 0.3 0.5 0.7
# AWS mod 0.9 nm 0.1 0.3 0.5 0.7
# GCP mod 0.0 nm 0.0 0.9
# GCP mod 0.1 nm 0.0 0.9
# GCP mod 0.3 nm 0.0 0.9
# GCP mod 0.5 nm 0.0 0.9
# GCP mod 0.7 nm 0.0 0.9
# GCP mod 0.9 nm 0.0 0.9
