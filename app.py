import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from math_engine import (
    generate_tensor_grid, 
    run_optimized_solver, 
    run_pareto_optimization, 
    verify_rbac_permission, 
    fetch_materials_api_data, 
    app_predict
)

# Page Configuration
st.set_page_config(
    page_title="I-TRE | TensorLab Advanced Informatics",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Dark Mode Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #161b22;
    }
    h1, h2, h3 {
        color: #58a6ff;
    }
    .metric-card {
        background-color: #1f6feb;
        padding: 20px;
        border-radius: 10px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .api-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .rbac-badge {
        background-color: #238636;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
    </style>
""", unsafe_allow_html=True)

# Authentication & RBAC State Management
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = "Junior Researcher"

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🔒 TensorLab Enterprise RBAC Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Select your enterprise clearance level and authenticate.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_role = st.selectbox("Assign User Role", ["Junior Researcher", "Senior Materials Scientist", "Enterprise Admin"])
        password = st.text_input("Access Password", type="password", placeholder="Enter demo123")
        
        if st.button("Authenticate Session", use_container_width=True):
            if password == "demo123":
                st.session_state.authenticated = True
                st.session_state.user_role = selected_role
                st.rerun()
            else:
                st.error("Invalid access code. Use `demo123`.")
    st.stop()

# Header
st.title("🧪 Inverse Tensor Reconstructive Engine (I-TRE v5.1 RBAC Edition)")
st.markdown(f"### Multiscale Informatics Hub | Active Role: <span class='rbac-badge'>{st.session_state.user_role}</span>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR: ENTERPRISE CONFIGURATION ---
st.sidebar.header("⚙️ Enterprise Pipeline Config")

with st.sidebar.expander("👤 User Session & Role", expanded=True):
    st.sidebar.markdown(f"**Logged in as:** `{st.session_state.user_role}`")
    if st.sidebar.button("Switch User / Logout"):
        st.session_state.authenticated = False
        st.rerun()

with st.sidebar.expander("🌐 Materials REST API Connector", expanded=True):
    db_source = st.selectbox("Data Source API", ["Materials Project REST API", "PubChem Crystal DB", "Synthetic Generator"])
    
    # RBAC check for API Key input modification
    if verify_rbac_permission(st.session_state.user_role, "api_keys"):
        api_key_input = st.text_input("API Key (Production)", type="password", value="demo_key")
    else:
        st.sidebar.warning("🔒 Restricted: Using Managed Enterprise Key")
        api_key_input = "demo_key"

with st.sidebar.expander("⚛️ Periodic Table Elements", expanded=True):
    selected_elements = st.multiselect(
        "Constituent Elements",
        ["Carbon (C)", "Silicon (Si)", "Aluminum (Al)", "Titanium (Ti)", "Oxygen (O)", "Hydrogen (H)", "Nitrogen (N)", "Iron (Fe)"],
        default=["Carbon (C)", "Silicon (Si)", "Oxygen (O)"]
    )

with st.sidebar.expander("⚙️ Solver Performance Settings", expanded=False):
    tensor_rank = st.slider("Tensor Resolution Rank", min_value=10, max_value=80, value=30, step=5)
    
    # RBAC check for advanced solver tuning
    if verify_rbac_permission(st.session_state.user_role, "advanced_solvers"):
        inversion_tolerance = st.selectbox("Inversion Tolerance", [1e-3, 1e-4, 1e-5], index=1)
        optimizer_method = st.selectbox("SciPy Optimization Routine", ["Nelder-Mead", "BFGS", "Powell"])
    else:
        st.sidebar.info("ℹ️ Standard Preset Active (Admin required for custom tolerances)")
        inversion_tolerance = 1e-4
        optimizer_method = "Nelder-Mead"

# --- SECTION 2: CONTROL CENTER & MAIN SCREEN INPUT BOXES ---
st.subheader("📐 Enterprise Control Center & Multi-Objective Solver")

col_ctrl, col_res = st.columns([1, 1])

with col_ctrl:
    st.markdown("#### 🎛️ Multivariable Main Screen Input Boxes")
    
    tensor_scaling_factor = st.number_input("Tensor Scale Factor", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    curing_temp_input = st.number_input("Curing Temperature (°C)", min_value=20.0, max_value=300.0, value=150.0, step=5.0)
    initial_alpha_guess = st.number_input("Initial Alpha Guess", value=1.0, step=0.1)
    initial_beta_guess = st.number_input("Initial Beta Guess", value=1.0, step=0.1)
    prediction_query = st.text_input("Compound Signature Query:", "SiO2-RBAC-01")
    
    run_solver_btn = st.button("Execute Enterprise RBAC Pipeline", use_container_width=True)

# Fetch data and run solvers
api_result = fetch_materials_api_data(api_key_input, prediction_query)
x_vals, y_vals, X, Y, Z = generate_tensor_grid(tensor_rank, tensor_scaling_factor, curing_temp_input)
weights, strengths, masses, efficiencies = run_pareto_optimization(tensor_rank, curing_temp_input)

with col_res:
    st.markdown("#### 📊 Solver Output & RBAC Metrics")
    
    st.markdown(f"""
        <div class="api-card">
            <p style="color: #58a6ff; font-weight: bold; margin-bottom: 5px;">🌐 API Connector Status: {api_result.get('status')}</p>
            <p style="color: #8b949e; font-size: 13px; margin: 0;"><b>Source:</b> {api_result.get('source')} | <b>Access Level:</b> {st.session_state.user_role}</p>
        </div>
    """, unsafe_allow_html=True)

    opt_alpha, opt_beta, opt_residual = run_optimized_solver(
        Z, X, Y, optimizer_method, inversion_tolerance, initial_alpha_guess, initial_beta_guess
    )
    
    st.markdown(f"""
        <div class="metric-card">
            <h4>RBAC Clearance Status: Verified ✅</h4>
            <p><b>Max Efficiency Index:</b> {max(efficiencies):.4f} | <b>Residual Error:</b> {opt_residual:.6f}</p>
        </div>
    """, unsafe_allow_html=True)
    
    results_df = pd.DataFrame({
        "Parameter Metric": ["Alpha Coefficient", "Beta Coefficient", "Max Strength Score", "Min Mass/Cost Score", "Curing Temp"],
        "Value": [f"{opt_alpha:.4f}", f"{opt_beta:.4f}", f"{max(strengths):.2f} MPa", f"{min(masses):.2f} g/cm³", f"{curing_temp_input}°C"]
    })
    st.dataframe(results_df, use_container_width=True)
    
    # --- CSV & JSON EXPORT UTILITIES ---
    st.markdown("#### 💾 Export Enterprise Package")
    csv_data = results_df.to_csv(index=False).encode('utf-8')
    json_data = json.dumps({
        "architecture": "Phase 2 RBAC Multi-User Enterprise",
        "user_role": st.session_state.user_role,
        "api_connector_data": api_result,
        "compound_signature": prediction_query,
        "selected_elements": selected_elements,
        "optimization_results": {
            "alpha": opt_alpha,
            "beta": opt_beta,
            "residual_error": opt_residual
        }
    }, indent=4).encode('utf-8')

    export_col1, export_col2 = st.columns(2)
    with export_col1:
        st.download_button("Download CSV Report", data=csv_data, file_name=f"{prediction_query}_rbac_report.csv", mime="text/csv", use_container_width=True)
    with export_col2:
        st.download_button("Download JSON Package", data=json_data, file_name=f"{prediction_query}_rbac_package.json", mime="application/json", use_container_width=True)

# --- SECTION 1: VISUALIZATIONS & PARETO FRONTIER ---
st.markdown("---")
col_v1, col_v2, col_v3 = st.columns(3)

with col_v1:
    st.subheader("🔥 2D Spatial Stress")
    fig_2d = px.imshow(Z, x=x_vals, y=y_vals, color_continuous_scale="Viridis")
    fig_2d.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ffffff", margin=dict(l=10, r=10, t=20, b=10), height=300)
    st.plotly_chart(fig_2d, use_container_width=True)

with col_v2:
    st.subheader("🧊 3D Volumetric State")
    fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Plasma")])
    fig_3d.update_layout(
        scene=dict(xaxis=dict(backgroundcolor="#161b22", gridcolor="#30363d"),
                   yaxis=dict(backgroundcolor="#161b22", gridcolor="#30363d"),
                   zaxis=dict(backgroundcolor="#161b22", gridcolor="#30363d")),
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ffffff", margin=dict(l=0, r=0, t=20, b=0), height=300
    )
    st.plotly_chart(fig_3d, use_container_width=True)

with col_v3:
    st.subheader("📈 Pareto Frontier")
    fig_pareto = px.scatter(x=masses, y=strengths, color=efficiencies,
                            labels=dict(x="Mass / Cost Score", y="Mechanical Strength (MPa)", color="Efficiency"),
                            color_continuous_scale="Turbo")
    fig_pareto.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ffffff", margin=dict(l=10, r=10, t=20, b=10), height=300)
    st.plotly_chart(fig_pareto, use_container_width=True)

# --- SECTION 3: PREDICTION OUTCOMES LINKED TO ELEMENTS ---
st.markdown("---")
st.subheader("🔬 RBAC-Validated DFT Mapped Elements")

if prediction_query:
    predicted_elements = app_predict(prediction_query, selected_elements, curing_temp_input)
    st.markdown(f"**Calculated Elements for Query:** `{prediction_query}` (Authorized for `{st.session_state.user_role}`)")
    
    cols = st.columns(len(predicted_elements))
    for idx, element in enumerate(predicted_elements):
        with cols[idx]:
            st.markdown(f"""
                <div style="background-color: #161b22; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; min-height: 90px;">
                    <p style="color: #8b949e; font-size: 11px; margin-bottom: 3px;">Node {idx+1}</p>
                    <p style="color: #58a6ff; font-weight: bold; font-size: 13px; margin: 0;">{element}</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e;'>TensorLab Engine v5.1 Phase 2 | Role-Based Access Control Enterprise Edition</p>", unsafe_allow_html=True)
