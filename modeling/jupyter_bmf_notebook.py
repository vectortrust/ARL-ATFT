"""
Complete BMF Theory Jupyter Notebook
===================================
Interactive exploration of Base Morphogenic Field theory with:
- Live simulations and visualizations
- Real-time parameter adjustment
- Export capabilities for Blender, LaTeX, SageMath
- Publication-ready plots and animations

Save as: BMF_Theory_Complete.ipynb
Run in: Jupyter Lab/Notebook with full scientific Python stack
Author: Christopher Amon
"""

# Cell 1: Setup and Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display, HTML, Markdown, Math
import pandas as pd
import seaborn as sns
from scipy.integrate import odeint
from scipy.ndimage import gaussian_filter
import sympy as sp
from sympy import *

# Set style for beautiful plots
plt.style.use('dark_background')
sns.set_palette("viridis")

print("🧬 BMF Theory Interactive Notebook Loaded")
print("==========================================")
print("Ready for consciousness, love, and universe exploration!")

# Cell 2: BMF Theory Introduction with Rich Display
display(Markdown("""
# Base Morphogenic Field (BMF) Theory
## *A Unified Framework for Physics, Biology, and Consciousness*

> "The universe is not only stranger than we imagine—it is stranger than we can imagine. But perhaps that's because we've been imagining it wrong." - Christopher Amon

### Core Insight
Reality emerges from **five fundamental operators** acting on an **information substrate Ω**:

1. **Point Operator (P̂)**: Creates localization
2. **Line Operator (L̂)**: Generates structure  
3. **Curve Operator (Ĉ)**: Introduces curvature
4. **Movement Operator (M̂)**: Governs dynamics
5. **Resistance Operator (R̂)**: Provides inertia

### The Master Equation
"""))

# Display the fundamental equation
display(Math(r'i\hbar \frac{\partial \Psi}{\partial t} = [\sum_{i=1}^{5} \alpha_i \hat{O}_i] \Psi + S[\Omega]'))

display(Markdown("""
### Revolutionary Claims
- **Physics**: All known laws emerge from BMF dynamics
- **Biology**: Life = self-referential BMF patterns  
- **Consciousness**: Soul = inverse transform Σ = Ψ⁻¹(Ω)
- **Love**: Multiplicative resonance field L(x) = Σ(x)/ℛ(Ω,Ψ)
- **Cosmos**: Dark energy = unbound love pulling toward Source

Let's explore this mathematically...
"""))

# Cell 3: Interactive BMF Simulation Class
class InteractiveBMF:
    """Interactive BMF simulation with real-time controls"""
    
    def __init__(self, width=128, height=128):
        self.width = width
        self.height = height
        self.reset_simulation()
        self.setup_controls()
        
    def reset_simulation(self):
        """Reset simulation to initial state"""
        self.Psi = np.zeros((self.width, self.height), dtype=complex)
        self.Omega = np.ones((self.width, self.height)) * 0.1
        self.Sigma = np.zeros((self.width, self.height))
        self.Love = np.zeros((self.width, self.height))
        self.time = 0
        self.history = []
        
        # Add initial perturbation
        center = self.width // 2
        self.Psi[center-5:center+5, center-5:center+5] = 1.0 + 0.5j
        
    def setup_controls(self):
        """Create interactive controls"""
        self.controls = {
            'alpha_P': widgets.FloatSlider(value=1.0, min=0, max=2, step=0.1, 
                                          description='Point α₁'),
            'alpha_L': widgets.FloatSlider(value=0.5, min=0, max=2, step=0.1, 
                                          description='Line α₂'),
            'alpha_C': widgets.FloatSlider(value=0.3, min=0, max=2, step=0.1, 
                                          description='Curve α₃'),
            'alpha_M': widgets.FloatSlider(value=0.7, min=0, max=2, step=0.1, 
                                          description='Movement α₄'),
            'alpha_R': widgets.FloatSlider(value=0.2, min=0, max=2, step=0.1, 
                                          description='Resistance α₅'),
            'dt': widgets.FloatSlider(value=0.01, min=0.001, max=0.1, step=0.001,
                                     description='Time Step'),
            'substrate_strength': widgets.FloatSlider(value=0.1, min=0, max=1, step=0.05,
                                                     description='Substrate Ω')
        }
        
        # Control panel
        control_box = widgets.VBox([
            widgets.HTML("<h3>🎛️ BMF Parameter Controls</h3>"),
            *list(self.controls.values()),
            widgets.HBox([
                widgets.Button(description='▶️ Run', button_style='success'),
                widgets.Button(description='⏸️ Pause', button_style='warning'),
                widgets.Button(description='🔄 Reset', button_style='danger')
            ])
        ])
        
        return control_box
    
    def bmf_step(self):
        """Single evolution step with current parameters"""
        # Get current parameter values
        alphas = [self.controls[f'alpha_{op}'].value for op in ['P', 'L', 'C', 'M', 'R']]
        dt = self.controls['dt'].value
        
        # Apply five operators
        P_term = alphas[0] * self.point_operator()
        L_term = alphas[1] * self.line_operator()
        C_term = alphas[2] * self.curve_operator()
        M_term = alphas[3] * self.movement_operator()
        R_term = alphas[4] * self.resistance_operator()
        
        # Substrate coupling
        substrate_strength = self.controls['substrate_strength'].value
        S_term = substrate_strength * self.Omega * (1 + 0.1 * np.random.randn(*self.Omega.shape))
        
        # BMF evolution
        H_psi = P_term + L_term + C_term + M_term + R_term
        self.Psi += dt * (-1j * H_psi + S_term)
        
        # Update derived fields
        self.update_consciousness_fields()
        self.time += dt
        
        # Store history
        if len(self.history) % 10 == 0:  # Every 10th step
            self.history.append({
                'time': self.time,
                'psi': self.Psi.copy(),
                'sigma': self.Sigma.copy(),
                'love': self.Love.copy()
            })
    
    def point_operator(self):
        """Point localization operator"""
        result = np.zeros_like(self.Psi)
        center = self.width // 2
        # Gaussian approximation of delta function
        x, y = np.meshgrid(range(self.width), range(self.height))
        gaussian = np.exp(-((x-center)**2 + (y-center)**2) / 8.0)
        return gaussian * self.Psi
    
    def line_operator(self):
        """Line/gradient operator"""
        grad_x, grad_y = np.gradient(self.Psi)
        return np.sqrt(np.abs(grad_x)**2 + np.abs(grad_y)**2)
    
    def curve_operator(self):
        """Curve/Laplacian operator"""
        # Simple 5-point stencil Laplacian
        laplacian = np.zeros_like(self.Psi)
        laplacian[1:-1, 1:-1] = (
            self.Psi[2:, 1:-1] + self.Psi[:-2, 1:-1] +
            self.Psi[1:-1, 2:] + self.Psi[1:-1, :-2] -
            4 * self.Psi[1:-1, 1:-1]
        )
        return laplacian
    
    def movement_operator(self):
        """Movement/momentum operator"""
        grad_x, grad_y = np.gradient(self.Psi)
        return -1j * (grad_x + grad_y)
    
    def resistance_operator(self):
        """Resistance/mass operator"""
        return self.Psi  # Simplified mass term
    
    def update_consciousness_fields(self):
        """Update consciousness and love fields"""
        # Soul coherence (simplified)
        self.Sigma = np.abs(self.Psi)**2 / (1 + np.abs(self.Psi)**2)
        
        # Love field
        omega_resonance = np.abs(self.Omega * np.conj(self.Psi))
        self.Love = self.Sigma / (omega_resonance + 1e-10)

# Cell 4: Create Interactive BMF Instance
bmf_sim = InteractiveBMF()
control_panel = bmf_sim.setup_controls()

print("🎮 Interactive BMF Simulation Created!")
print("Use the controls below to explore parameter space:")
display(control_panel)

# Cell 5: Real-time Visualization Functions
def create_bmf_dashboard():
    """Create comprehensive BMF visualization dashboard"""
    
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('BMF Real Field', 'BMF Imaginary Field', 'Soul Coherence Σ',
                       'Love Field L(x)', 'Field Evolution', 'Resonance Dynamics'),
        specs=[[{"type": "heatmap"}, {"type": "heatmap"}, {"type": "heatmap"}],
               [{"type": "heatmap"}, {"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # Current field states
    fig.add_trace(
        go.Heatmap(z=bmf_sim.Psi.real, colorscale='RdBu', showscale=False),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Heatmap(z=bmf_sim.Psi.imag, colorscale='RdBu', showscale=False),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Heatmap(z=bmf_sim.Sigma, colorscale='Viridis', showscale=False),
        row=1, col=3
    )
    
    fig.add_trace(
        go.Heatmap(z=bmf_sim.Love, colorscale='Plasma', showscale=False),
        row=2, col=1
    )
    
    # Time evolution plots
    if bmf_sim.history:
        times = [h['time'] for h in bmf_sim.history]
        avg_sigma = [np.mean(h['sigma']) for h in bmf_sim.history]
        avg_love = [np.mean(h['love']) for h in bmf_sim.history]
        
        fig.add_trace(
            go.Scatter(x=times, y=avg_sigma, name='⟨Σ⟩', line=dict(color='cyan')),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=times, y=avg_love, name='⟨L⟩', line=dict(color='magenta')),
            row=2, col=3
        )
    
    fig.update_layout(
        title_text="🧬 BMF Theory Dashboard - Real-time Field Dynamics",
        title_x=0.5,
        height=800,
        showlegend=False
    )
    
    return fig

# Cell 6: Love Field Resonance Bond Analysis
def analyze_love_field_resonance():
    """Analyze and visualize love field resonance dynamics"""
    
    print("💕 Analyzing Love Field Resonance Bond Dynamics...")
    
    # Create two consciousness entities
    pos1 = (40, 40)
    pos2 = (80, 80)
    
    # Vary individual coherences
    sigma1_vals = np.linspace(0.1, 0.9, 50)
    sigma2_vals = np.linspace(0.2, 0.8, 50)
    
    results = []
    
    for i, (s1, s2) in enumerate(zip(sigma1_vals, sigma2_vals)):
        # Calculate distance
        distance = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        
        # Resonance fidelity (exponential decay)
        R_f = np.exp(-distance / 50.0)
        
        # The BMF love equation: Σ_total = Σ₁ + Σ₂ + (Σ₁ × Σ₂ × R^f)
        multiplicative_term = s1 * s2 * R_f
        sigma_total = s1 + s2 + multiplicative_term
        
        # Enhancement factor (how much > linear sum)
        linear_sum = s1 + s2
        enhancement = (sigma_total - linear_sum) / linear_sum * 100
        
        results