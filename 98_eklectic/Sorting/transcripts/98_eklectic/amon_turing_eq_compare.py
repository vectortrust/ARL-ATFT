# Amon-Turing Field Theory vs Foundational Differential Equations

# --- Setup Symbolics ---
from sage.all import var, function, diff, integrate, simplify, solve, latex
from IPython.display import display, Math

# Variables
x, t, m, v, F, phi, c = var('x t m v F phi c')

# --- 1. Newton's Second Law ---
F_eq = F == m * diff(v, t)
display(Math("F = m \, \frac{dv}{dt} = %s" % latex(F_eq)))

# --- 2. Wave Equation ---
phi = function('phi')(x, t)
wave_eq = diff(phi, t, 2) == c^2 * diff(phi, x, 2)
display(Math("\frac{\partial^2 \, \phi}{\partial t^2} = c^2 \, \frac{\partial^2 \, \phi}{\partial x^2} = %s" % latex(wave_eq)))

# --- 3. Klein-Gordon Equation ---
m, hbar = var('m hbar')
kge = diff(phi, t, 2) - c^2 * diff(phi, x, 2) + (m^2 * c^4 / hbar^2) * phi == 0
display(Math("\text{Klein-Gordon: }" + latex(kge)))

# --- 4. Amon-Turing Field Placeholder ---
# Your symbolic field expression (replace placeholder)
A = function('A')(x, t)
AT_field = diff(A, t, 2) - diff(A, x, 2) + A^3 == 0
display(Math("\text{Amon-Turing: }" + latex(AT_field)))

# --- Numeric Integration Example: Newton's Law ---
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# m = 1, F = constant = 10 => dv/dt = 10
f_num = lambda v, t: 10
v0 = 0
t_vals = np.linspace(0, 10, 100)
v = odeint(f_num, v0, t_vals)

plt.plot(t_vals, v)
plt.title("Numerical Integration of Newton's Second Law")
plt.xlabel("Time t")
plt.ylabel("Velocity v(t)")
plt.grid(True)
plt.savefig("newton_velocity.pdf")
plt.show()

# --- Save to .npy for Blender ---
np.save("./newton_velocity.npy", v)

# --- Export Note ---
# Use Jupyter Export > PDF or:
# !jupyter nbconvert --to pdf amon_turing_eq_compare.ipynb

print("Notebook ready: symbolic equations, numerical test, Blender export, PDF-capable")
