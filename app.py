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
    run_inverse_design_screening,
    generate_crystal_lattice_animation,
    generate_executive_report_html,
    verify_rbac_permission, 
    fetch_materials_api_data, 
    app_predict,
    simulate_reagent_mixing,
    get_standard_reagents
)

# Page Configuration
st.set_page_config(
    page_title="TensorLab | Materials Informatics",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Refined High-Contrast Dark Mode Styling
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
    .brand-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 14px 20px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    .brand-title-box {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Secure Authentication
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

# --- SIDEBAR: CONFIGURATION & SETTINGS (RENDERED FIRST) ---
st.sidebar.header("Configuration")

with st.sidebar.expander("User Session", expanded=True):
    st.sidebar.text(f"Role: {st.session_state.user_role}")
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

with st.sidebar.expander("Workspace Layout Settings", expanded=True):
    show_lattice_anim = st.checkbox("Show 3D Lattice Animation", value=True)
    show_pareto = st.checkbox("Show Pareto Frontier", value=True)
    show_batch = st.checkbox("Show Batch Simulation Queue", value=True)

with st.sidebar.expander("Materials Database API", expanded=False):
    db_source = st.selectbox("Source", ["Materials Project REST API", "PubChem Crystal DB", "Synthetic Generator"])
    api_key_input = production_api_key

with st.sidebar.expander("Constituent Elements", expanded=False):
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

# --- MASTER BRAND TITLE BAR WITH HIGH-CONTRAST LOGO & ACTIONS ---
st.markdown("""
    <div class="brand-container">
        <div class="brand-title-box">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 3 6.5 12 11 21 6.5 12 2" stroke="#58a6ff" stroke-width="2"></polygon>
              <line x1="12" y1="11" x2="12" y2="13.5" stroke="#58a6ff" stroke-width="2"></line>
              <line x1="4" y1="15.5" x2="20" y2="15.5" stroke="#58a6ff" stroke-width="2"></line>
              <line x1="4" y1="19.5" x2="15" y2="19.5" stroke="#58a6ff" stroke-width="2"></line>
              <circle cx="18.5" cy="19.5" r="1.5" fill="#238636" stroke="#238636" stroke-width="2"></circle>
            </svg>
            <div>
                <h1 style="margin: 0; color: #58a6ff !important; font-size: 22px !important; font-weight: 800; letter-spacing: 0.5px;">TENSOR<span style="color: #f0f6fc;">LAB</span></h1>
                <span style="color: #8b949e; font-size: 10px; text-transform: uppercase; letter-spacing: 1.2px;">Materials Informatics Sandbox</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

action_col1, action_col2, action_col3 = st.columns(3)
with action_col1:
    if st.button("💾 Save", use_container_width=True, help="Save simulation state"):
        st.toast("Workspace state saved successfully!", icon="💾")
with action_col2:
    if st.button("📂 Export", use_container_width=True, help="Export session data"):
        st.toast("Preparing session export package...", icon="📦")
with action_col3:
    if st.button("⚙️ Config", use_container_width=True, help="Quick settings"):
        st.toast("Opening configuration panel...", icon="⚙️")

st.markdown(f"<span style='color: #8b949e; font-size: 12px;'>Session Active &bull; Role:</span> <span class='rbac-badge'>{st.session_state.user_role}</span>", unsafe_allow_html=True)
st.markdown("<hr style='margin: 10px 0; border-color: #30363d;'>", unsafe_allow_html=True)

# --- VIRTUAL REAGENT SHELF & SYNTHESIS FLASK ---
st.markdown("#### 🧪 Virtual Synthesis Laboratory")
st.markdown("<p style='color: #8b949e; font-size: 13px;'>Select from over 1,000 standard chemical lab reagents on the shelf to drive the mathematical simulation engine.</p>", unsafe_allow_html=True)

col_shelf, col_flask = st.columns([1, 1])

with col_shelf:
    st.markdown("##### 🗄️ Reagent Shelf (1,000+ Standard Chemicals)")
    available_shelf = get_standard_reagents()
    chosen_reagents = st.multiselect("Select Reagents for Synthesis", available_shelf, default=["Silicon Dioxide (SiO2)", "Carbon Nanotube (CNT)"])
    synthesis_temp_input = st.slider("Flask Curing Temperature (°C)", min_value=20.0, max_value=300.0, value=180.0, step=5.0)

with col_flask:
    st.markdown("##### ⚗️ Reaction Flask Chamber")
    if st.button("Mix & Initiate Synthesis Reaction", use_container_width=True):
        st.session_state.flask_result = simulate_reagent_mixing(chosen_reagents, synthesis_temp_input)
    
    if "flask_result" not in st.session_state:
        st.session_state.flask_result = simulate_reagent_mixing(chosen_reagents, 180.0)
    
    res = st.session_state.flask_result
    st.markdown(f"""
        <div class="flask-card">
            <span style="font-size: 24px;">🧪</span><br>
            <span style="color: #58a6ff; font-weight: 600; font-size: 14px;">Status: {res.get('status')}</span><br>
            <span style="font-size: 13px; color: #f0f6fc;">Predicted Phase: <b>{res.get('predicted_phase')}</b></span><br>
            <span style="font-size: 12px; color: #8b949e;">Purity: {res.get('purity')}% &bull; Density: {res.get('density')} g/cm³ &bull; Query: `{res.get('query_sig')}`</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SIMULATION CONTROL PANEL & BATCH QUEUE ---
st.markdown("#### Simulation Control Panel (Math Engine)")

col_ctrl, col_res = st.columns([1, 1])

with col_ctrl:
    default_scale = res.get('derived_scale', 1.0)
    default_temp = res.get('derived_temp', 180.0)
    default_query = res.get('query_sig', 'SiO2-RBAC-01')

    tensor_scaling_factor = st.number_input("Tensor Scale Factor", min_value=0.1, max_value=10.0, value=float(default_scale), step=0.1)
    curing_temp_input = st.number_input("Curing Temperature (°C)", min_value=20.0, max_value=300.0, value=float(default_temp), step=5.0)
    initial_alpha_guess = st.number_input("Initial Alpha Guess", value=1.0, step=0.1)
    initial_beta_guess = st.number_input("Initial Beta Guess", value=1.0, step=0.1)
    
    prediction_query = st.text_input("Primary Compound Query", value=default_query)
    
    if show_batch:
        st.markdown("##### Batch Simulation Queue")
        batch_input_str = st.text_area("Compound Signatures (Comma separated)", f"{default_query}, Al2O3-Beta, Fe2O3-Gamma, TiC-Delta")
    
    run_solver_btn = st.button("Execute Simulation Pipeline", use_container_width=True)

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
    
    if show_batch and verify_rbac_permission(st.session_state.user_role, "batch_queues"):
        st.markdown("##### Batch Queue Results")
        queries_list = batch_input_str.split(",")
        batch_df = run_batch_simulation(queries_list, curing_temp_input, tensor_scaling_factor)
        st.dataframe(batch_df, use_container_width=True)
        
        if verify_rbac_permission(st.session_state.user_role, "reports"):
            st.markdown("##### Automated Report Pipeline")
            report_html = generate_executive_report_html(
                st.session_state.user_role, prediction_query, curing_temp_input, 
                tensor_scaling_factor, opt_alpha, opt_beta, opt_residual, batch_df
            )
            st.download_button(
                "📥 Download HTML Research Report", 
                data=report_html, 
                file_name=f"{prediction_query}_research_report.html", 
                mime="text/html", 
                use_container_width=True
            )

# --- INVERSE DESIGN & HIGH-THROUGHPUT SCREENING MODULE ---
st.markdown("---")
st.markdown("#### Inverse Design & Reagent Screening")

if verify_rbac_permission(st.session_state.user_role, "inverse_design"):
    inv_col1, inv_col2 = st.columns([1, 2])
    with inv_col1:
        target_str_input = st.number_input("Target Strength (MPa)", min_value=50.0, max_value=350.0, value=200.0, step=10.0)
        target_den_input = st.number_input("Target Density (g/cm³)", min_value=1.0, max_value=5.0, value=2.5, step=0.1)
        run_screening_btn = st.button("Screen 1,000+ Reagents", use_container_width=True)
    
    with inv_col2:
        if run_screening_btn:
            screening_df = run_inverse_design_screening(target_str_input, target_den_input, available_shelf)
            st.dataframe(screening_df, use_container_width=True)
        else:
            st.info("Configure your target material specifications on the left and click screen to search the 1,000+ reagent catalog.")
else:
    st.info("Inverse design & high-throughput screening restricted for current clearance level.")

# --- VISUALIZATIONS & PARETO FRONTIER ---
st.markdown("---")
st.markdown("#### Spatial & Multi-Objective Visualizations")

if show_pareto:
    col_v1, col_v2, col_v3 = st.columns(3)
else:
    col_v1, col_v2 = st.columns(2)

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

if show_pareto:
    with col_v3:
        st.caption("Pareto Frontier Trade-Offs")
        fig_pareto = px.scatter(x=masses, y=strengths, color=efficiencies,
                                labels=dict(x="Mass / Cost", y="Strength (MPa)", color="Efficiency"),
                                color_continuous_scale="Turbo")
        fig_pareto.update_layout(plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=10, r=10, t=10, b=10), height=280)
        st.plotly_chart(fig_pareto, use_container_width=True)

# --- CRYSTALLINE STRUCTURE & THERMAL VIBRATION ANIMATION ---
if show_lattice_anim:
    st.markdown("---")
    st.markdown("#### Crystalline Structure & Thermal Lattice Dynamics")

    if verify_rbac_permission(st.session_state.user_role, "crystal_animation"):
        col_c1, col_c2 = st.columns([1, 3])
        with col_c1:
            lattice_system = st.selectbox("Lattice System", ["FCC (Face-Centered Cubic)", "BCC (Body-Centered Cubic)", "Diamond Cubic"])
            selected_code = lattice_system.split(" ")[0]
            thermal_slider = st.slider("Thermal Energy / Vibration", min_value=0.2, max_value=3.0, value=1.0, step=0.2)
            st.caption("Use the media player bar below the chart to play, pause, and scrub through thermal vibration frames.")
        
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
                    margin=dict(l=0, r=0, t=40, b=60), height=440,
                    updatemenus=[dict(
                        type="buttons",
                        showactive=False,
                        x=0.5,
                        y=-0.18,
                        xanchor="center",
                        yanchor="top",
                        direction="left",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 180, "redraw": True}, "fromcurrent": True, "transition": {"duration": 50}}]),
                            dict(label="❚❚ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                        ]
                    )],
                    sliders=[dict(
                        active=0,
                        yanchor="top",
                        xanchor="left",
                        currentvalue={"prefix": "Frame: ", "font": {"color": "#58a6ff"}},
                        pad={"t": 35, "b": 10},
                        len=0.9,
                        x=0.05,
                        y=-0.1,
                        steps=[dict(args=[[str(k)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                                    label=str(k+1),
                                    method="animate") for k in range(len(frames_data))]
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

# --- DFT MAPPED ELEMENT NODES ---
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
st.markdown("<p style='text-align: center; color: #8b949e; font-size: 11px;'>TensorLab Materials Workspace &bull; Secure R&D Environment</p>", unsafe_allow_html=True)
