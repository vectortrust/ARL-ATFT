# bmf_universe.py
# Initial simulation logic for BMF field evolution
# Author: Christopher R. Amon (ORCID: 0000-0001-9133-7677)

import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
size = 100
P_field = np.zeros((size, size))
P_field[size//2, size//2] = 1  # Initial central activation

def evolve(P, k=0.05, Lambda=0.01):
    # Line Operator (L): discrete Laplacian (4-neighbor)
    L = np.roll(P, 1, axis=0) + np.roll(P, -1, axis=0) + \
        np.roll(P, 1, axis=1) + np.roll(P, -1, axis=1) - 4 * P

    # Movement Operator (M): temporal change
    M = P - evolve.prev

    # Resistance Operator (R): damping proportional to M
    R = -k * M

    # Curve Operator (C): same as L in discrete 2D
    C = L

    evolve.prev = P.copy()
    return P + 0.1 * (C + M + R + Lambda)

evolve.prev = P_field.copy()

# --- Visualization Loop ---
if __name__ == "__main__":
    import time
    from IPython.display import clear_output

    for _ in range(100):
        P_field = evolve(P_field)
        clear_output(wait=True)
        plt.imshow(P_field, cmap='viridis')
        plt.title("BMF Universe v0.1")
        plt.colorbar()
        plt.show()
        time.sleep(0.1)
