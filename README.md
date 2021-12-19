# ITER Fusion Reactor Blanket Optimization for Tritium Breeding using OpenMC

This repository is part of undergraduate thesis by Husni Naufal Zuhdi to pursue nuclear engineering degree in Nuclear Engineering and Physics Engineering Departement at Universitas Gadjah Mada.

## Abstract

The present world energy source is still heavily dependent on fossil energy. Nuclear fusion energy from deuterium and tritium is one of the high-density energy sources. Deuterium is abundant in seawater, but tritium is limited. International Thermonuclear Experimental Reactor (ITER) is one of the biggest nuclear fusion projects in the world. Nuclear fusion reactor needs tritium breeding blanket to fulfil tritium requirement. Tritium Breeding Ratio (TBR) represents a ratio between tritium production and tritium consumption in a nuclear fusion reactor. This undergraduate thesis aims is to gain optimal design for the ITER fusion reactor blanket.

TBR simulation done using OpenMC and Paramak programs. Blanket fluid material used in this undergraduate thesis is lithium fluoride with 6Li enrichment variation in these values 10%, 30%, 50%, 70%, and 90%. To increase TBR value in ITER breeder blanket design graphite moderator and natural lead neutron multiplier were added into ITER breeder blanket design. Addition of moderator volume taking place part of main fluid breeder blanket volume while the addition of neutron multiplier volume taking place part of moderator volume. Variation of moderator volume ratio against main fluid breeder blanket volume done in these values 0.1, 0.3, 0.5, 0.7 and 0.9 while variation of neutron multiplier volume ratio against moderator volume done in these values 0.1, 0.3, 0.5, 0.7 and 0.9.

The result of the ITER breeder blanket design simulation shows that the most optimal 6Li enrichment, moderator volume ratio, and neutron multiplier volume ratio configuration sequentially is 70%, 0.5, and 0.9 with TBR value in the amount of 1.005552 ± 0.004294.

## How to Use
For Windows user, please [install WSL2](https://docs.microsoft.com/en-gb/windows/wsl/install-win10) in your computer before moving forward to the next step. It will provide a linux sub system in your Windows OS environment.

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

## Aditional
You can see my undergraduate thesis and presentation files in thesis folder

## Important links for learning
[OpenMC Discourse Group](https://openmc.discourse.group/)

[OpenMC Google Chat Group](https://groups.google.com/g/openmc-users)

[Paramak Neutronic Youtube Quick Tutorial](https://youtu.be/40VARwD44FA)

## License
This repository use [MIT License](https://raw.githubusercontent.com/hazunanafaru/iter-tritium-breeding-xgboost/main/LICENSE).
