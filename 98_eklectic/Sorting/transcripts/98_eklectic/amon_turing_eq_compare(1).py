# Amon-Turing Equation Notebook (Converted from Outline)

# --- 1. Symbolic Derivation (SageMath) ---
from sage.all import var, diff, integrate, simplify, function, latex
from IPython.display import display, Math

x, t = var('x t')
A = function('A')(x, t)
AT_field = diff(A, t, 2) - diff(A, x, 2) + A^3 == 0

display(Math(r"\text{Amon-Turing Field: }" + latex(AT_field)))

# --- 2. Numerical Integration (SciPy/Numpy) ---
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

f = lambda v, t: 10
v0 = 0
t_vals = np.linspace(0, 10, 100)
v = odeint(f, v0, t_vals)

plt.plot(t_vals, v)
plt.title("Numerical Integration of Newton's Law")
plt.xlabel("t")
plt.ylabel("v(t)")
plt.grid(True)
plt.savefig("newton_velocity.pdf")
plt.show()

# --- 3. Amon-Turing Core Simulation (Placeholder) ---
import sys
sys.path.append('/home/nfs/wip/stack')

import bmf_simulation_core

try:
    results = bmf_simulation_core.run_simulation()
    np.save("amon_turing_results.npy", results)
    print("Simulation complete.")
except Exception as e:
    print("Simulation failed:", e)

# --- 4. OpenCL Acceleration Test ---
import pyopencl as cl
import pyopencl.array as cl_array

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

N = 1024
a = np.random.rand(N).astype(np.float32)
b = np.random.rand(N).astype(np.float32)

a_g = cl_array.to_device(queue, a)
b_g = cl_array.to_device(queue, b)
c_g = a_g + b_g

print("First few results:", c_g[:5].get())
np.save("opencl_sum.npy", c_g.get())
