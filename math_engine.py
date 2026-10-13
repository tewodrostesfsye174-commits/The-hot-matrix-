import numpy as np
import streamlit as st
from scipy.optimize import minimize

@st.cache_data
def generate_tensor_grid(rank, scale, temp):
    """Generates the 2D spatial stress distribution and 3D volumetric matrix."""
    x_vals = np.linspace(-5, 5, rank)
    y_vals = np.linspace(-5, 5, rank)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = scale * (temp / 150.0) * np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))
    return x_vals, y_vals, X, Y, Z

@st.cache_data
def run_optimized_solver(Z_target, X_grid, Y_grid, method, tol, alpha_guess, beta_guess):
    """Executes cached SciPy inverse optimization minimization."""
    def objective_func(params):
        a, b = params
        return np.sum((Z_target - (a * np.sin(X_grid) + b * np.cos(Y_grid)))**2)
    
    initial_guess = [alpha_guess, beta_guess]
    res = minimize(objective_func, initial_guess, method=method, tol=tol)
    return float(res.x[0]), float(res.x[1]), float(res.fun)

def app_predict(query_str, elements_list, temp):
    """Maps compound signatures to simulated DFT outcome elements."""
    np.random.seed(abs(hash(query_str)) % (2**32))
    base_elements = [
        f"DFT-Optimized Matrix ({elements_list[0] if elements_list else 'C'})",
        f"Cross-linked Prepolymer Backbone (Temp: {temp}°C)",
        f"Secondary Element Phase ({elements_list[1] if len(elements_list)>1 else 'Si'})",
        "Silane Coupling Interfacial Agent",
        "Amine-Functionalized Curing Catalyst"
    ]
    return base_elements[:4]
