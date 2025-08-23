#!/bin/bash
# install_bmf_stack.sh
# BMF Unified Modeling Environment Setup for Ubuntu 22.04+

set -e

# Update system
sudo apt update && sudo apt upgrade -y

# Core packages
sudo apt install -y python3 python3-pip python3-venv build-essential git wget curl \
    libgl1-mesa-glx libxrender1 libxext6 libsm6 libglu1-mesa

# Create venv
python3 -m venv ~/bmf_env
source ~/bmf_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core Python packages
pip install numpy scipy matplotlib sympy plotly pandas tqdm \
            pint networkx h5py pyvista mayavi

# Install JAX (CPU-only)
pip install jax jaxlib

# Install FEniCSx (via Docker)
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
mkdir -p ~/fenicsx_projects
cd ~/fenicsx_projects
docker pull dolfinx/dolfinx:latest

# Optional: Blender (for visualizations)
sudo snap install blender --classic

# Clone BMF starter code
cd ~
git clone https://github.com/example/BMF-Simulator.git  # Replace with real repo later

# Done
echo "\n✅ BMF modeling environment ready. Activate with:"
echo "source ~/bmf_env/bin/activate"
echo "Run FEniCSx inside Docker with:"
echo "docker run -ti -v \$HOME/fenicsx_projects:/home/fenics/shared -w /home/fenics/shared dolfinx/dolfinx"
