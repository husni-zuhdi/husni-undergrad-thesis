import numpy as np
import pandas as pd
import csv as csv
import os

# Set Cloud Storage Service Account
from google.cloud import storage
client = storage.Client.from_service_account_json('key.json', project='iter-tritium-breeding-xgboost')

# Set variables of result file
enrich_lis = [0.1, 0.3, 0.5, 0.7, 0.9]
mod_ratios = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9]
neutron_multis = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9]
bucket = client.bucket("iter-tritium-breeding-xgboost-bucket") # Your bucket name
result_uri = "v3/results/" # Result.json files uri

# Download all result.json file in Cloud Storage Bucket
for enrich_li in enrich_lis:
    for mod_ratio in mod_ratios:
        for neutron_multi in neutron_multis:
            try:
                print("Downloading : " + str(enrich_li) + "-" + str(mod_ratio) + "-" + str(neutron_multi) + "-20-5000.json")
                blob = bucket.blob(result_uri + str(enrich_li) + "-" + str(mod_ratio) + "-" + str(neutron_multi) + "-20-5000.json")
                blob.download_to_filename("result/" + str(enrich_li) + "-" + str(mod_ratio) + "-" + str(neutron_multi) + "-20-5000.json")
            except Exception:
                pass

# Read folder contain simulation results
path = "/home/ubuntu/iter-tritium-breeding-xgboost/jupyter-notebooks/2-data-analysis/result" # Change this path
results = os.listdir(path=path)
results.sort()

# Read data in each folder
data = []
for result in results:
    # Find enrichment feature
    folder_path = path + str(result)
    folder_list = result.split('-')
    folder_list = folder_list[0:3]
    
    # Read tbr and std dev data
    try:
        json_result = pd.read_json(path + "/" + result)
        json_result = json_result["blanket_fluid_mat_(n,Xt)"]["events per source particle"]
        data.append([folder_list[0], folder_list[1], folder_list[2], json_result['result'], json_result['std. dev.']])
    except Exception:
        pass

# Build dataframe from simulation data
df = pd.DataFrame(data, columns=['Li6_enrichment', 'Moderator_ratio','Neutron_multiplier', 'Tbr_OpenMC', 'Stddev'])

# Convert all dataframe type from string into float
df.Li6_enrichment = df.Li6_enrichment.astype(float)
df.Moderator_ratio = df.Moderator_ratio.astype(float)
df.Neutron_multiplier = df.Neutron_multiplier.astype(float)

# Export dataframe to csv
df.to_csv("iter_tritium_breeding.csv", index=False)

# Export an excel file
datatoexcel = pd.ExcelWriter('df.xlsx')
df.to_excel(datatoexcel)
datatoexcel.save()