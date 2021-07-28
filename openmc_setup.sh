cd /tasks
git clone https://github.com/openmc-dev/openmc.git
cd /tasks/openmc

# Install v.0.13.0.dev0 with DAGMCUniverse Class
git checkout develop
mkdir /tasks/openmc/build
cd /tasks/openmc/build
cmake -Ddagmc=ON ..
make
make install
PATH="$PATH:/tasks/openmc/build/bin"
cp /tasks/openmc/build/bin/openmc /usr/local/bin

cd /tasks/openmc
pip install .