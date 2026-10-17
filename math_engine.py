import numpy as np
import pandas as pd

def generate_tensor_grid(rank, scale, temp):
    x = np.linspace(-scale, scale, rank)
    y = np.linspace(-scale, scale, rank)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2) * (temp / 100.0)) * np.cos(X) * scale
    return x, y, X, Y, Z

def run_optimized_solver(Z, X, Y, routine, tolerance, alpha_guess, beta_guess):
    residual = float(np.mean(np.abs(Z)) * tolerance * 10)
    opt_alpha = float(alpha_guess + np.max(X) * 0.05)
    opt_beta = float(beta_guess + np.min(Y) * 0.05)
    return opt_alpha, opt_beta, residual

def compute_elastic_tensor_matrix(tensor_rank, scale, temp):
    c11 = round(210.5 + (scale * 12.0) - (temp * 0.05), 2)
    c12 = round(65.2 + (scale * 4.1), 2)
    c44 = round(75.8 + (temp * 0.08), 2)
    bulk_modulus = round((c11 + 2 * c12) / 3.0, 2)
    shear_modulus = round((c11 - c12 + 3 * c44) / 5.0, 2)
    poisson_ratio = round(c12 / (c11 + c12), 3)
    return {
        "C11 (GPa)": c11, "C12 (GPa)": c12, "C44 (GPa)": c44,
        "Bulk Modulus K": bulk_modulus, "Shear Modulus G": shear_modulus, "Poisson's Ratio ν": poisson_ratio
    }

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

def run_inverse_design_screening(targets, reagents_list):
    results = []
    np.random.seed(42)
    t_strength = targets.get("strength", 200.0)
    t_density = targets.get("density", 2.5)
    t_viscosity = targets.get("viscosity", 1000.0)
    t_conductivity = targets.get("conductivity", 0.01)
    t_tg = targets.get("tg", 80.0)

    for r in reagents_list[:120]:
        sim_strength = round(np.random.uniform(50, 350), 2)
        sim_density = round(np.random.uniform(1.0, 4.5), 2)
        sim_viscosity = round(np.random.uniform(50, 5000), 2)
        sim_conductivity = round(np.random.uniform(0.0001, 0.5), 4)
        sim_tg = round(np.random.uniform(-20, 200), 1)
        
        match_score = round(100 - (
            abs(sim_strength - t_strength) * 0.15 +
            abs(sim_density - t_density) * 10.0 +
            abs(sim_viscosity - t_viscosity) * 0.002 +
            abs(sim_conductivity - t_conductivity) * 20.0 +
            abs(sim_tg - t_tg) * 0.1
        ), 2)
        
        if match_score > 30:
            results.append({
                "Reagent Candidate": r,
                "Est. Strength (MPa)": sim_strength,
                "Est. Density (g/cm³)": sim_density,
                "Est. Viscosity (cP)": sim_viscosity,
                "Est. Conductivity (S/cm)": sim_conductivity,
                "Match Score (%)": max(0.0, match_score)
            })
    df_res = pd.DataFrame(results)
    if not df_res.empty:
        return df_res.sort_values(by="Match Score (%)", ascending=False).head(10)
    return pd.DataFrame(columns=["Reagent Candidate", "Est. Strength (MPa)", "Est. Density (g/cm³)", "Est. Viscosity (cP)", "Est. Conductivity (S/cm)", "Match Score (%)"])

def generate_crystal_lattice_animation(lattice_type="FCC", thermal_factor=1.0):
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
    else:
        base_coords = np.array([
            [0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
            [0.25, 0.25, 0.25], [0.75, 0.75, 0.25], [0.75, 0.25, 0.75], [0.25, 0.75, 0.75]
        ])
    frames_data = []
    np.random.seed(100)
    for i in range(15):
        noise = np.sin(i * 0.5) * 0.08 * thermal_factor * np.random.randn(*base_coords.shape)
        frames_data.append(base_coords + noise)
    return base_coords, frames_data

def get_standard_reagents():
    categories = ["Oxide", "Carbide", "Nitride", "Precursor", "Halide", "Sulfate", "Nitrate", "Phosphate", "Polymer", "Solvent", "Silicate", "Titanate", "Boride", "Complex"]
    elements = ["Li", "Na", "K", "Mg", "Ca", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Al", "Si", "Ga", "Ge", "Zr", "Nb", "Mo", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Y", "La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"]
    
    reagents = [
        "Silicon Dioxide (SiO2)", "Titanium Carbide (TiC)", "Aluminum Precursor (Al2O3)", 
        "Carbon Nanotube (CNT)", "Iron Oxide (Fe2O3)", "Nitrogen Stabilizer (N2)",
        "Graphene Oxide (GO)", "Boron Nitride (BN)", "Tungsten Carbide (WC)", "Silicon Carbide (SiC)"
    ]
    counter = 11
    for el in elements:
        for cat in categories:
            for val in [1, 2, 3]:
                if len(reagents) < 1000:
                    reagents.append(f"{el} {cat} Grade-{val} (Ref-{counter:04d})")
                    counter += 1
    while len(reagents) < 1000:
        reagents.append(f"Synthetic Lab Reagent Spec-{len(reagents)+1} (High-Purity)")
    return reagents

def simulate_reagent_mixing(selected_reagents, curing_temp):
    reagent_count = len(selected_reagents)
    if reagent_count == 0:
        return {
            "status": "Empty Flask", "purity": 0.0, "density": 0.0, 
            "predicted_phase": "None", "derived_temp": curing_temp, 
            "derived_scale": 1.0, "query_sig": "EMPTY-FLASK"
        }
    base_purity = min(99.9, 85.0 + (reagent_count * 1.2) - (abs(curing_temp - 150) * 0.05))
    base_density = round(2.2 + (reagent_count * 0.2), 2)
    derived_scale = round(1.0 + (reagent_count * 0.05) + (curing_temp / 500.0), 2)
    phases = ["FCC Crystalline Matrix", "BCC Intermetallic Lattice", "Diamond Cubic Composite", "Amorphous Polymer Network"]
    selected_phase = phases[hash(tuple(selected_reagents)) % len(phases)]
    query_sig = f"SYNTH-BATCH-{reagent_count}comps-{int(curing_temp)}C"
    return {
        "status": "Reaction Successful & Mapped to Math Engine",
        "purity": round(base_purity, 2),
        "density": base_density,
        "predicted_phase": selected_phase,
        "derived_temp": curing_temp,
        "derived_scale": derived_scale,
        "query_sig": query_sig,
        "reagents_used": selected_reagents
    }

def verify_rbac_permission(role, feature):
    permissions = {
        "Junior Researcher": ["crystal_animation"],
        "Senior Materials Scientist": ["crystal_animation", "advanced_solvers", "batch_queues", "inverse_design"],
        "Enterprise Admin": ["crystal_animation", "advanced_solvers", "batch_queues", "reports", "inverse_design", "elastic_tensor"]
    }
    return feature in permissions.get(role, [])

def generate_executive_report_html(role, query, temp, scale, alpha, beta, residual, batch_df):
    return f"""
    <html>
    <head><title>Research Report - {query}</title></head>
    <body style="font-family: sans-serif; background: #0b0f19; color: #f0f6fc; padding: 25px;">
        <h2 style="color: #58a6ff;">TensorLab Executive Research Report</h2>
        <p><b>Query Signature:</b> {query}</p>
        <p><b>User Clearance Role:</b> {role}</p>
        <p><b>Curing Temperature:</b> {temp}°C | <b>Tensor Scale Factor:</b> {scale}</p>
        <p><b>Solver Convergence:</b> Alpha: {alpha:.4f}, Beta: {beta:.4f}, Residual: {residual:.6f}</p>
        <hr style="border-color: #30363d;">
        <h3 style="color: #58a6ff;">Batch Results Summary</h3>
        {batch_df.to_html()}
    </body>
    </html>
    """
