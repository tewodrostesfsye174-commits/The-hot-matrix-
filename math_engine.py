import numpy as np
import pandas as pd
import json

def generate_tensor_grid(rank, scale, temp):
    x = np.linspace(-scale, scale, rank)
    y = np.linspace(-scale, scale, rank)
    X, Y = np.meshgrid(x, y)
    # Z represents spatial stress/strain distribution influenced by temperature
    Z = np.sin(np.sqrt(X**2 + Y**2) * (temp / 100.0)) * np.cos(X) * scale
    return x, y, X, Y, Z

def run_optimized_solver(Z, X, Y, routine, tolerance, alpha_guess, beta_guess):
    # Simulated numerical solver convergence based on inputs
    residual = float(np.mean(np.abs(Z)) * tolerance * 10)
    opt_alpha = float(alpha_guess + np.max(X) * 0.05)
    opt_beta = float(beta_guess + np.min(Y) * 0.05)
    return opt_alpha, opt_beta, residual

def run_pareto_optimization(rank, temp):
    np.random.seed(42)
    weights = np.linspace(10, 100, rank)
    strengths = weights * 2.5 + np.random.normal(0, 5, rank) + (temp * 0.2)
    masses = weights * 0.8 + np.random.normal(0, 2, rank)
    efficiencies = strengths / (masses + 1e-5)
    return weights, strengths, masses, efficiencies

def run_batch_simulation(queries, temp, scale):
    data = []
    for q in queries:
        q_clean = q.strip()
        score = round(len(q_clean) * 1.5 + temp * 0.05 * scale, 2)
        data.append({"Compound Signature": q_clean, "Curing Temp (°C)": temp, "Predicted Score": score, "Status": "Converged"})
    return pd.DataFrame(data)

def generate_crystal_lattice_animation(lattice_type="FCC", thermal_factor=1.0):
    # Base coordinates for unit cell lattices
    if lattice_type == "FCC":
        base_coords = np.array([
            [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
            [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1],
            [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
            [0.5, 0.5, 1], [0.5, 1, 0.5], [1, 0.5, 0.5]
        ])
    elif lattice_type == "BCC":
        base_coords = np.array([
            [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
            [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1],
            [0.5, 0.5, 0.5]
        ])
    else: # Diamond Cubic
        base_coords = np.array([
            [0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
            [0.25, 0.25, 0.25], [0.75, 0.75, 0.25], [0.75, 0.25, 0.75], [0.25, 0.75, 0.75]
        ])
    
    # Generate 15 thermal displacement frames for animation
    frames_data = []
    np.random.seed(100)
    for i in range(15):
        noise = np.sin(i * 0.5) * 0.08 * thermal_factor * np.random.randn(*base_coords.shape)
        frames_data.append(base_coords + noise)
        
    return base_coords, frames_data

def simulate_reagent_mixing(selected_reagents, curing_temp, scaling_factor):
    reagent_count = len(selected_reagents)
    if reagent_count == 0:
        return {"status": "Empty Flask", "purity": 0.0, "density": 0.0, "predicted_phase": "None"}
    
    base_purity = min(99.9, 85.0 + (reagent_count * 3.2) - (abs(curing_temp - 150) * 0.05))
    base_density = round(2.2 + (reagent_count * 0.4) * scaling_factor, 2)
    
    phases = ["FCC Crystalline Matrix", "BCC Intermetallic Lattice", "Diamond Cubic Composite", "Amorphous Polymer Network"]
    selected_phase = phases[hash(tuple(selected_reagents)) % len(phases)]
    
    return {
        "status": "Reaction Successful",
        "purity": round(base_purity, 2),
        "density": base_density,
        "predicted_phase": selected_phase,
        "reagents_used": selected_reagents
    }

def verify_rbac_permission(role, feature):
    permissions = {
        "Junior Researcher": ["crystal_animation"],
        "Senior Materials Scientist": ["crystal_animation", "advanced_solvers", "batch_queues"],
        "Enterprise Admin": ["crystal_animation", "advanced_solvers", "batch_queues", "reports"]
    }
    return feature in permissions.get(role, [])

def fetch_materials_api_data(api_key, query):
    return {"status": "Connected to External Enterprise API", "source": "Materials Project Gateway"}

def app_predict(query, elements, temp):
    return [
        f"DFT-Optimized Matrix ({elements[0] if elements else 'Carbon'})",
        f"Cross-linked Prepolymer Backbone (Temp:{temp}°C)",
        f"Secondary Element Phase ({elements[1] if len(elements) > 1 else 'Silicon'})",
        "Silane Coupling Interfacial Agent"
    ]

def generate_executive_report_html(role, query, temp, scale, alpha, beta, residual, batch_df):
    return f"""
    <html>
    <head><title>Executive Report - {query}</title></head>
    <body style="font-family: sans-serif; background: #0b0f19; color: #f0f6fc; padding: 20px;">
        <h2>TensorLab Executive Report</h2>
        <p><b>Query Signature:</b> {query}</p>
        <p><b>User Clearance Role:</b> {role}</p>
        <p><b>Curing Temperature:</b> {temp}°C | <b>Scale Factor:</b> {scale}</p>
        <p><b>Solver Results:</b> Alpha: {alpha:.4f}, Beta: {beta:.4f}, Residual: {residual:.6f}</p>
        <hr>
        <h3>Batch Results Summary</h3>
        {batch_df.to_html()}
    </body>
    </html>
    """
