# Optimization of ITER Blanket Design for Tritium Breeding Using Monte Carlo Method Coupled with Machine Learning

This repository is part of undergraduate thesis by Husni Naufal Zuhdi (413821) to pursue nuclear engineering degree in Nuclear Engineering and Physics Engineering Departement at Universitas Gadjah Mada.

## Description

## How to Use
For Windows user, please [install WSL2](https://docs.microsoft.com/en-gb/windows/wsl/install-win10) in your computer before moving forward to the next step.
It will provide a linux sub system in your Windows OS environment.

For Linux and macOS user :
1. Download or Clone this repository.
2. Run [`openmc_setup_rev.sh`](https://raw.githubusercontent.com/hazunanafaru/iter-tritium-breeding-xgboost/main/openmc_setup_rev.sh) in your terminal to install.
    - OpenMC with DAGMC dependencies.
    - Paramak, Paramak Neutronics and Neutronics Mateiral Maker.
    - ENDF-VIII.0 Nuclear Database.
    - XGBoost, scikit-learn, numpy, matplotlib, and any machine learning tools needed.
    - Jupyter Lab.
3. (Optional) If you want to use Google Cloud Service SDK (gcloud, gsutil, etc) run [`install_gcloud_and_gsutil.sh`](https://raw.githubusercontent.com/hazunanafaru/iter-tritium-breeding-xgboost/main/install_gcloud_and_gsutil.sh).
4. Run this code to launch jupyter lab in your web browser
```
   jupyter lab --ip 0.0.0.0 --port 8888 --no-browser
```
5. If you run the code in local, click the link showed in terminal. If you run the cloud in the cloud, go to `http://<your_instance_public_ip>:8888` and insert the given token.
6. Run the code you want to learn.


## Important links for learning
[OpenMC Discourse Group](https://openmc.discourse.group/)

[OpenMC Google Chat Group](https://groups.google.com/g/openmc-users)

[Paramak Neutronic Youtube Quick Tutorial](https://youtu.be/40VARwD44FA)

## License
This repository use [MIT License](https://raw.githubusercontent.com/hazunanafaru/iter-tritium-breeding-xgboost/main/LICENSE).
