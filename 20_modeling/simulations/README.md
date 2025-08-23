# ATFT Simulations

This folder contains simple 2D simulations to explore operator dynamics and generate figures/metrics for the dissertation.

## atft_sim2d.py
A damped wave-like PDE on a 2D grid that maps the operators to numerical terms:

- Curve operator C → spatial Laplacian ∇²P
- Movement operator M → time derivative ∂P/∂t
- Resistance operator R → damping term −k·∂P/∂t
- Point operator P̂ → localized source term S(x,y,t)

Master form (discretized):

    ∂²P/∂t² = c² ∇²P − k ∂P/∂t + S

Outputs:
- `npz` file containing final field and basic time series metrics
- CSV summary of energy and coherence proxy per step (optional)
 - Optional PGM image of the final field for quick inspection

Usage:

    python atft_sim2d.py --nx 128 --ny 128 --steps 1000 \
      --dt 1e-3 --dx 1.0 --c 1.0 --k 0.02 \
      --source gaussian --src-amp 1.0 --src-sigma 3.0 --out run1 --save-pgm

This produces `run1.npz` with arrays and `run1_metrics.csv` with per-step metrics.

Energy check (conservative limit; sanity metric):

    python atft_sim2d.py --steps 2000 --k 0 --out energy_check --check-energy

This prints a relative energy variation and writes `energy_check_energy_check.txt`. With simple explicit schemes and periodic boundaries this is only a sanity indicator; more accurate conservation follows from smaller time steps and improved integrators.
