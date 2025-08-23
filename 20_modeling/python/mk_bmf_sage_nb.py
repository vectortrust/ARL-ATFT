import nbformat as nbf
nb = nbf.v4.new_notebook()
nb['metadata']['kernelspec'] = {
  "display_name": "SageMath",
  "language": "sage",
  "name": "sage"
}
cells = []

cells += [nbf.v4.new_code_cell(r"""
# --- symbols + operators ---
var('x y t')
P = function('P')(x,y,t)

# coefficients (dimensionful scaling kept external)
var('a_c a_m a_r Lambda k')

gradP   = (diff(P,x), diff(P,y))
lapP    = diff(P,x,2) + diff(P,y,2)        # curvature C
Mop     = diff(P,t)                         # movement M
Rop     = -k*diff(P,t)                      # resistance R

Master  = diff(P,t,2) - (a_c*lapP + a_m*Mop + a_r*Rop + Lambda)   # LHS form = 0

show(Master)
print(latex(Master))
""")]

cells += [nbf.v4.new_code_cell(r"""
# --- test field: gaussian pulse ---
var('sigma omega')
assume(sigma>0, omega>0)
Ptest = exp(-(x^2 + y^2)/sigma^2) * cos(omega*t)

Res = Master.subs({P:Ptest}).simplify_full()
show(Res)
print(latex(Res))
""")]

cells += [nbf.v4.new_code_cell(r"""
# --- energy-like form (multiply by ∂P/∂t) ---
Pt = diff(P,t)
Energy_like = ( Pt*diff(P,t,2) - Pt*(a_c*lapP + a_m*diff(P,t) + a_r*(-k*diff(P,t)) + Lambda) ).simplify_full()
show(Energy_like)
print(latex(Energy_like))
""")]

cells += [nbf.v4.new_code_cell(r"""
# --- quick LaTeX export helper ---
def tex(name, expr):
    print(f"% --- {name} ---"); print(latex(expr)); print()

tex('Gradient', gradP)
tex('Laplacian', lapP)
tex('Movement M', Mop)
tex('Resistance R', Rop)
tex('MasterEq', Master)
""")]

cells += [nbf.v4.new_code_cell(r"""
# --- pick simple coeffs and evaluate residual ---
subs0 = {a_c:1, a_m:1, a_r:1, k:0.1, Lambda:0}
show( Master.subs(subs0) )
show( Master.subs(subs0).subs({P:Ptest}).simplify_full() )
""")]

nb['cells'] = cells
with open("bmf_operators.ipynb","w") as f: nbf.write(nb,f)
print("Wrote bmf_operators.ipynb")
