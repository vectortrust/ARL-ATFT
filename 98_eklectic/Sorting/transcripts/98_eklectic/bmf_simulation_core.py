#!/bin/bash
# install_bmf_stack.sh
# Optimized BMF Unified Modeling Environment Setup for Debian 13 (KDE + Wayland)

set -e

# Update system
sudo apt update && sudo apt upgrade -y

# Required Mesa/OpenGL libs
sudo apt install -y libgl1 libglx-mesa0 libgl1-mesa-dri libgl1-mesa-dev \
    mesa-utils mesa-vulkan-drivers

# Intel GPU monitoring
sudo apt install -y intel-gpu-tools

# Optional: OpenCL support (for physics kernel offload)
sudo apt install -y ocl-icd-libopencl1 intel-opencl-icd clinfo

# Swapfile setup (8GB)
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo "/swapfile none swap sw 0 0" | sudo tee -a /etc/fstab

# Core development tools
sudo apt install -y python3 python3-pip python3-venv build-essential git curl \
    libsm6 libxrender1 libxext6 libglu1-mesa

# Python virtual environment
python3 -m venv ~/bmf_env
source ~/bmf_env/bin/activate
pip install --upgrade pip

# Python packages
pip install numpy scipy matplotlib sympy plotly pandas tqdm \
            pint networkx h5py pyvista mayavi pyopencl

# Install JAX (CPU-only)
pip install jax jaxlib

# Install FEniCSx via Docker
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
mkdir -p ~/fenicsx_projects
cd ~/fenicsx_projects
docker pull dolfinx/dolfinx:latest

# Blender for advanced rendering
sudo snap install blender --classic

# Clone BMF starter code (replace with real URL)
cd ~
git clone https://github.com/example/BMF-Simulator.git

# Done
clear
echo "\n✅ BMF modeling environment ready. To activate Python env:"
echo "source ~/bmf_env/bin/activate"
echo "To run FEniCSx in Docker:"
echo "docker run -ti -v \$HOME/fenicsx_projects:/home/fenics/shared -w /home/fenics/shared dolfinx/dolfinx"
echo "To monitor GPU: sudo intel_gpu_top"
echo "To test OpenCL: clinfo | grep 'Intel'"
