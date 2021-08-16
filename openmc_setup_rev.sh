#!/bin/bash
echo INSTALL MINICONDA
echo ======================
read -p "Press any key to resume ..."
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
cd ~/
mkdir miniconda
cd ~/miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh
bash Miniconda3-py38_4.10.3-Linux-x86_64.sh -b -u -p ~/miniconda3
cd ~/
rm -r ~/miniconda
source ~/.bashrc

echo INSTALL ipykernel
echo ======================
read -p "Press any key to resume ..."
source ~/.bashrc
conda init bash
conda activate base
conda install ipykernel -y
ipython kernel install --user --name=base

echo INSTALL CMAKE, LAPACK, BLAS, EIGEN3, HDF5, AND GFORTRAN
echo ======================
read -p "Press any key to resume ..."
sudo apt-get install cmake libblas-dev liblapack-dev libeigen3-dev libhdf5-dev gfortran python3-pip -y

echo INSTALL CADQUERY2 and PYTHON REQUIREMENTS
echo ======================
read -p "Press any key to resume ..."
sudo apt-get update
sudo apt-get install ffmpeg libsm6 libxext6  -y
cd ~/iter-tritium-breeding-xgboost
pip3 install -r jupyter-notebooks/requirements.txt
conda install -c cadquery -c conda-forge cadquery=master -y
export PATH="~/.local/bin:$PATH"

echo INSTALL MOAB
echo ======================
read -p "Press any key to resume ..."
cd ~/
mkdir ~/MOAB
cd ~/MOAB
git clone -b Version5.1.0 https://bitbucket.org/fathomteam/moab/
cd ~/MOAB
mkdir ~/MOAB/build
cd ~/MOAB/build
cmake ../moab -DENABLE_HDF5=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=~/MOAB -DENABLE_PYMOAB=ON
export PYTHONPATH=~/MOAB/lib/python3.8/site-packages/:$PYTHONPATH
make
make test install
cd pymoab
python3 setup.py install
export LD_LIBRARY_PATH=~/MOAB/lib:$LD_LIBRARY_PATH

echo INSTALL DAGMC
echo ======================
read -p "Press any key to resume ..."
cd ~/
mkdir ~/DAGMC
cd ~/DAGMC
git clone -b develop https://github.com/svalinn/dagmc
cd ~/DAGMC
mkdir ~/DAGMC/build
cd ~/DAGMC/build
cmake ../dagmc -DBUILD_TALLY=ON -DCMAKE_INSTALL_PREFIX=/home/$USER/DAGMC -DMOAB_DIR=/home/$USER/MOAB -DBUILD_STATIC_LIBS=OFF
make install
rm -rf ~/DAGMC/dagmc
env LD_LIBRARY_PATH=~/DAGMC/lib:$LD_LIBRARY_PATH


# %env FC=mpif90
# %env CC=mpicc

echo INSTALL OPENMC
echo ======================
read -p "Press any key to resume ..."
cd ~/
git clone https://github.com/openmc-dev/openmc.git
cd ~/openmc
mkdir ~/openmc/build
cd ~/openmc/build
cmake -Ddagmc=ON -DCMAKE_PREFIX_PATH=~/DAGMC ..
make
sudo make install
export PATH="$PATH:~/openmc/build/bin"
sudo cp ~/openmc/build/bin/openmc /usr/local/bin

cd ~/openmc
pip3 install .

echo DOWNLOAD ENDF/B-VIII.0 NUCLEAR DATA
echo ======================
read -p "Press any key to resume ..."
cd ~/
mkdir ~/ND
wget -O ~/ND/endfb80.tar.xz https://anl.box.com/shared/static/uhbxlrx7hvxqw27psymfbhi7bx7s6u6a.xz
cd ~/ND
tar -xvf endfb80.tar.xz
rm endfb80.tar.xz

echo SET NUCLEAR DATA VARIABLE
echo ======================
read -p "Press any key to resume ..."
cd ~/
echo "# OpenMC Nuclear Database ENDF VIII.o" >> ~/.bashrc
echo "export OPENMC_CROSS_SECTIONS='/home/$USER/ND/endfb80_hdf5/cross_sections.xml'" >> ~/.bashrc
source ~/.bashrc

echo INSTALL JUPYTERLAB
echo ======================
read -p "Press any key to resume ..."
sudo pip3 install jupyterlab
sudo jupyter serverextension enable --py jupyterlab --sys-prefix
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser
