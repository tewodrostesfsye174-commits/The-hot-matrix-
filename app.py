import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from math_engine import (
    generate_tensor_grid, 
    run_optimized_solver, 
    run_pareto_optimization, 
    run_batch_simulation,
    generate_crystal_lattice_animation,
    generate_executive_report_html,
    verify_rbac_permission, 
    fetch_materials_api_data, 
    app_predict,
    simulate_reagent_mixing
)

# Page Configuration
st.set_page_config(
    page_title="TensorLab | Materials Informatics",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Refined High-Contrast Enterprise Dark Mode Styling (Deep Navy-Slate Palette)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f0f6fc;
    }
    .sidebar .sidebar-content, [data-testid="stSidebar"] {
        background-color: #111625;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #58a6ff !important;
        font-weight: 700;
    }
    p, span, label, .stMarkdown, .stText, div[data-baseweb="select"] {
        color: #f0f6fc !important;
    }
    .metric-card {
        background-color: #1f6feb;
        padding: 15px;
        border-radius: 8px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
    }
    .flask-card {
        background-color: #161b22;
        border: 2px dashed #58a6ff;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
    }
    .api-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .rbac-badge {
        background-color: #238636;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
    .dataframe {
        background-color: #161b22 !important;
        color: #f0f6fc !important;
    }
    </style>
""", unsafe_allow_html=True)

# Secure Authentication (with guaranteed fallback to 'demo123')
try:
    stored_admin_password = st.secrets.get("ADMIN_PASSWORD", "demo123")
    production_api_key = st.secrets.get("API_KEY", "demo_key")
except Exception:
    stored_admin_password = "demo123"
    production_api_key = "demo_key"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = "Junior Researcher"

if not st.session_state.authenticated:
    st.markdown("<h3 style='text-align: center; color: #58a6ff;'>TensorLab Workspace Login</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 13px;'>Select your assigned clearance role to access the workspace.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_role = st.selectbox("User Role", ["Junior Researcher", "Senior Materials Scientist", "Enterprise Admin"])
        password = st.text_input("Access Password", type="password", placeholder="Enter demo123")
        
        if st.button("Authenticate", use_container_width=True):
            if password == stored_admin_password or password == "demo123":
                st.session_state.authenticated = True
                st.session_state.user_role = selected_role
                st.rerun()
            else:
                st.error("Invalid access code. Use `demo123`.")
    st.stop()

# Clean Professional Header
st.markdown("### TensorLab Enterprise Workspace")
st.markdown(f"<span style='color: #8b949e; font-size: 13px;'>Session Active &bull; Role:</span> <span class='rbac-badge'>{st.session_state.user_role}</span>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR: CONFIGURATION ---
st.sidebar.header("Configuration")

with st.sidebar.expander("User Session", expanded=True):
    st.sidebar.text(f"Role: {st.session_state.user_role}")
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

with st.sidebar.expander("Materials Database API", expanded=True):
    db_source = st.selectbox("Source", ["Materials Project REST API", "PubChem Crystal DB", "Synthetic Generator"])
    api_key_input = production_api_key

with st.sidebar.expander("Constituent Elements", expanded=True):
    selected_elements = st.multiselect(
        "Elements",
        ["Carbon (C)", "Silicon (Si)", "Aluminum (Al)", "Titanium (Ti)", "Oxygen (O)", "Hydrogen (H)", "Nitrogen (N)", "Iron (Fe)"],
        default=["Carbon (C)", "Silicon (Si)", "Oxygen (O)"]
    )

with st.sidebar.expander("Solver Parameters", expanded=False):
    tensor_rank = st.slider("Resolution Rank", min_value=10, max_value=80, value=30, step=5)
    
    if verify_rbac_permission(st.session_state.user_role, "advanced_solvers"):
        inversion_tolerance = st.selectbox("Tolerance", [1e-3, 1e-4, 1e-5], index=1)
        optimizer_method = st.selectbox("Routine", ["Nelder-Mead", "BFGS", "Powell"])
    else:
        inversion_tolerance = 1e-4
        optimizer_method = "Nelder-Mead"

# --- NEW SECTION: VIRTUAL REAGENT SHELF & SYNTHESIS FLASK ---
st.markdown("#### 🧪 Virtual Synthesis Laboratory")
st.markdown("<p style='color: #8b949e; font-size: 13px;'>Select chemical reagents from the shelf, load them into the reaction flask, and synthesize custom compound matrices.</p>", unsafe_allow_html=True)

col_shelf, col_flask = st.columns([1, 1])

with col_shelf:
    st.markdown("##### 🗄️ Reagent Shelf")
    available_shelf = [
        "Silicon Dioxide (SiO2)", "Titanium Carbide (TiC)", 
        "Aluminum Precursor (Al2O3)", "Carbon Nanotube (CNT)", 
        "Iron Oxide (Fe2O3)", "Nitrogen Stabilizer (N2)"
    ]
    chosen_reagents = st.multiselect("Select Reagents for Synthesis", available_shelf, default=["Silicon Dioxide (SiO2)", "Carbon Nanotube (CNT)"])
    synthesis_temp = st.slider("Flask Curing Temperature (°C)", min_value=20.0, max_value=300.0, value=180.0, step=5.0)

with col_flask:
    st.markdown("##### ⚗️ Reaction Flask Chamber")
    if st.button("Mix & Initiate Synthesis Reaction", use_container_width=True):
        st.session_state.flask_result = simulate_reagent_mixing(chosen_reagents, synthesis_temp, 1.2)
    
    if "flask_result" not in st.session_state:
        st.session_state.flask_result = {"status": "Ready to Mix", "purity": 0.0, "density": 0.0, "predicted_phase": "Awaiting Reaction", "reagents_used": []}
    
    res = st.session_state.flask_result
    st.markdown(f"""
        <div class="flask-card">
            <span style="font-size: 24px;">🧪</span><br>
            <span style="color: #58a6ff; font-weight: 600; font-size: 14px;">Status: {res.get('status')}</span><br>
            <span style="font-size: 13px; color: #f0f6fc;">Predicted Phase: <b>{res.get('predicted_phase')}</b></span><br>
            <span style="font-size: 12px; color: #8b949e;">Estimated Purity: {res.get('purity')}% &bull; Density: {res.get('density')} g/cm³</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SECTION 2: CONTROL PANEL & BATCH QUEUE ---
st.markdown("#### Simulation Control Panel")

col_ctrl, col_res = st.columns([1, 1])

with col_ctrl:
    tensor_scaling_factor = st.number_input("Tensor Scale Factor", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    curing_temp_input = st.number_input("Curing Temperature (°C)", min_value=20.0, max_value=300.0, value=150.0, step=5.0)
    initial_alpha_guess = st.number_input("Initial Alpha Guess", value=1.0, step=0.1)
    initial_beta_guess = st.number_input("Initial Beta Guess", value=1.0, step=0.1)
    
    prediction_query = st.text_input("Primary Compound Query", "SiO2-RBAC-01")
    
    st.markdown("##### Batch Simulation Queue")
    batch_input_str = st.text_area("Compound Signatures (Comma separated)", "SiO2-Alpha, Al2O3-Beta, Fe2O3-Gamma, TiC-Delta, SiC-Omega")
    
    run_solver_btn = st.button("Execute Simulation Pipeline", use_container_width=True)

# Fetch data and run solvers
api_result = fetch_materials_api_data(api_key_input, prediction_query)
x_vals, y_vals, X, Y, Z = generate_tensor_grid(tensor_rank, tensor_scaling_factor, curing_temp_input)
weights, strengths, masses, efficiencies = run_pareto_optimization(tensor_rank, curing_temp_input)

with col_res:
    st.markdown("#### Execution Results & Metrics")
    
    st.markdown(f"""
        <div class="api-card">
            <span style="color: #58a6ff; font-weight: 600; font-size: 13px;">API Status: {api_result.get('status')}</span><br>
            <span style="color: #8b949e; font-size: 12px;">Source: {api_result.get('source')}</span>
        </div>
    """, unsafe_allow_html=True)

    opt_alpha, opt_beta, opt_residual = run_optimized_solver(
        Z, X, Y, optimizer_method, inversion_tolerance, initial_alpha_guess, initial_beta_guess
    )
    
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-weight: 600; margin-bottom: 4px;">Optimization Converged</div>
            <div style="font-size: 13px; color: #f0f6fc;">Max Efficiency: {max(efficiencies):.4f} &bull; Residual: {opt_residual:.6f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    results_df = pd.DataFrame({
        "Parameter Metric": ["Alpha Coefficient", "Beta Coefficient", "Max Strength Score", "Min Mass/Cost Score", "Curing Temp"],
        "Value": [f"{opt_alpha:.4f}", f"{opt_beta:.4f}", f"{max(strengths):.2f} MPa", f"{min(masses):.2f} g/cm³", f"{curing_temp_input}°C"]
    })
    st.dataframe(results_df, use_container_width=True)
    
    if verify_rbac_permission(st.session_state.user_role, "batch_queues"):
        st.markdown("##### Batch Queue Results")
        queries_list = batch_input_str.split(",")
        batch_df = run_batch_simulation(queries_list, curing_temp_input, tensor_scaling_factor)
        st.dataframe(batch_df, use_container_width=True)
        
        if verify_rbac_permission(st.session_state.user_role, "reports"):
            st.markdown("##### Automated Executive Report Pipeline")
            report_html = generate_executive_report_html(
                st.session_state.user_role, prediction_query, curing_temp_input, 
                tensor_scaling_factor, opt_alpha, opt_beta, opt_residual, batch_df
            )
            st.download_button(
                "📥 Download Executive HTML Report", 
                data=report_html, 
                file_name=f"{prediction_query}_executive_report.html", 
                mime="text/html", 
                use_container_width=True
            )
    else:
        st.caption("Batch queues and automated reporting restricted.")

# --- SECTION 1: VISUALIZATIONS & PARETO FRONTIER ---
st.markdown("---")
st.markdown("#### Spatial & Multi-Objective Visualizations")
col_v1, col_v2, col_v3 = st.columns(3)

with col_v1:
    st.caption("2D Spatial Stress")
    fig_2d = px.imshow(Z, x=x_vals, y=y_vals, color_continuous_scale="Viridis")
    fig_2d.update_layout(plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=10, r=10, t=10, b=10), height=280)
    st.plotly_chart(fig_2d, use_container_width=True)

with col_v2:
    st.caption("3D Volumetric State")
    fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Plasma")])
    fig_3d.update_layout(
        scene=dict(xaxis=dict(backgroundcolor="#111625", gridcolor="#30363d"),
                   yaxis=dict(backgroundcolor="#111625", gridcolor="#30363d"),
                   zaxis=dict(backgroundcolor="#111625", gridcolor="#30363d")),
        plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=0, r=0, t=10, b=0), height=280
    )
    st.plotly_chart(fig_3d, use_container_width=True)

with col_v3:
    st.caption("Pareto Frontier Trade-Offs")
    fig_pareto = px.scatter(x=masses, y=strengths, color=efficiencies,
                            labels=dict(x="Mass / Cost", y="Strength (MPa)", color="Efficiency"),
                            color_continuous_scale="Turbo")
    fig_pareto.update_layout(plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=10, r=10, t=10, b=10), height=280)
    st.plotly_chart(fig_pareto, use_container_width=True)

# --- SECTION: CRYSTALLINE STRUCTURE & THERMAL VIBRATION ANIMATION ---
st.markdown("---")
st.markdown("#### Crystalline Structure & Thermal Lattice Dynamics")

if verify_rbac_permission(st.session_state.user_role, "crystal_animation"):
    col_c1, col_c2 = st.columns([1, 3])
    with col_c1:
        lattice_system = st.selectbox("Lattice System", ["FCC (Face-Centered Cubic)", "BCC (Body-Centered Cubic)", "Diamond Cubic"])
        selected_code = lattice_system.split(" ")[0]
        thermal_slider = st.slider("Thermal Energy / Vibration", min_value=0.2, max_value=3.0, value=1.0, step=0.2)
        st.caption("Use the ▶ Play button at the top-left of the 3D chart to run real-time thermal atomic vibrations.")
    
    with col_c2:
        base_coords, frames_data = generate_crystal_lattice_animation(lattice_type=selected_code, thermal_factor=thermal_slider)
        
        fig_crystal = go.Figure(
            data=[go.Scatter3d(
                x=base_coords[:, 0], y=base_coords[:, 1], z=base_coords[:, 2],
                mode='markers+text',
                marker=dict(size=12, color=base_coords[:, 2], colorscale='Viridis', opacity=0.9),
                text=[f"Atom {i+1}" for i in range(len(base_coords))],
                textposition="top center"
            )],
            layout=go.Layout(
                title=dict(text=f"3D Lattice Dynamics: {lattice_system}", font=dict(size=14)),
                scene=dict(
                    xaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5]),
                    yaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5]),
                    zaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5])
                ),
                plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc",
                margin=dict(l=0, r=0, t=40, b=0), height=400,
                updatemenus=[dict(
                    type="buttons",
                    showactive=False,
                    x=0.0,
                    y=1.15,
                    xanchor="left",
                    yanchor="top",
                    buttons=[
                        dict(label="▶ Play Vibration",
                             method="animate",
                             args=[None, {"frame": {"duration": 180, "redraw": True}, "fromcurrent": True, "transition": {"duration": 50}}]),
                        dict(label="❚❚ Pause",
                             method="animate",
                             args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                    ]
                )]
            ),
            frames=[go.Frame(
                data=[go.Scatter3d(
                    x=frame[:, 0], y=frame[:, 1], z=frame[:, 2],
                    mode='markers',
                    marker=dict(size=12, color=frame[:, 2], colorscale='Viridis', opacity=0.9)
                )],
                name=str(k)
            ) for k, frame in enumerate(frames_data)]
        )
        st.plotly_chart(fig_crystal, use_container_width=True)
else:
    st.info("Crystalline lattice animation restricted for current clearance level.")

# --- SECTION 3: PREDICTION OUTCOMES LINKED TO ELEMENTS ---
st.markdown("---")
st.markdown("#### DFT Mapped Element Nodes")

if prediction_query:
    predicted_elements = app_predict(prediction_query, selected_elements, curing_temp_input)
    st.caption(f"Active Query Signature: `{prediction_query}` (Authorized for `{st.session_state.user_role}`)")
    
    cols = st.columns(len(predicted_elements))
    for idx, element in enumerate(predicted_elements):
        with cols[idx]:
            st.markdown(f"""
                <div style="background-color: #111625; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; min-height: 80px;">
                    <span style="color: #8b949e; font-size: 11px;">Node {idx+1}</span><br>
                    <span style="color: #58a6ff; font-weight: 600; font-size: 12px;">{element}</span>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e; font-size: 11px;'>TensorLab Enterprise Workspace &bull; Secure R&D Environment</p>", unsafe_allow_html=True)
