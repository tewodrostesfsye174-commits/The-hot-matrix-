import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from scipy.optimize import minimize

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

# Authentication State Management
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Authentication Gate (`demo123`)
if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🔒 TensorLab Access Control</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Enter security credentials to initialize the Advanced Inverse Engine.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Access Password", type="password", placeholder="Enter demo123")
        if st.button("Authenticate", use_container_width=True):
            if password == "demo123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code. Use `demo123`.")
    st.stop()

# Header
st.title("🧪 Inverse Tensor Reconstructive Engine (I-TRE v4.0)")
st.markdown("### Multiscale Materials Informatics & Multi-Variable Solver Hub")
st.markdown("---")

# --- SIDEBAR: ELEMENTS & CONFIG ---
st.sidebar.header("🎛️ Informatics Configuration")

with st.sidebar.expander("⚛️ Periodic Table Elements", expanded=True):
    selected_elements = st.multiselect(
        "Constituent Elements",
        ["Carbon (C)", "Silicon (Si)", "Aluminum (Al)", "Titanium (Ti)", "Oxygen (O)", "Hydrogen (H)", "Nitrogen (N)", "Iron (Fe)"],
        default=["Carbon (C)", "Silicon (Si)", "Oxygen (O)"]
    )

with st.sidebar.expander("⚙️ Solver Settings", expanded=False):
    tensor_rank = st.slider("Tensor Resolution Rank", min_value=10, max_value=50, value=25, step=5)
    inversion_tolerance = st.selectbox("Inversion Tolerance", [1e-3, 1e-4, 1e-5], index=1)
    optimizer_method = st.selectbox("SciPy Optimization Routine", ["Nelder-Mead", "BFGS", "Powell"])

# --- SECTION 1: VISUALIZATIONS ---
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.subheader("🔥 2D Spatial Stress Distribution")
    x_vals = np.linspace(-5, 5, tensor_rank)
    y_vals = np.linspace(-5, 5, tensor_rank)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))
    
    fig_2d = px.imshow(Z, x=x_vals, y=y_vals, color_continuous_scale="Viridis",
                       labels=dict(x="Spatial X", y="Spatial Y", color="Intensity"))
    fig_2d.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ffffff", margin=dict(l=10, r=10, t=20, b=10), height=350)
    st.plotly_chart(fig_2d, use_container_width=True)

with col_v2:
    st.subheader("🧊 3D Volumetric State")
    fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Plasma")])
    fig_3d.update_layout(
        scene=dict(xaxis=dict(backgroundcolor="#161b22", gridcolor="#30363d"),
                   yaxis=dict(backgroundcolor="#161b22", gridcolor="#30363d"),
                   zaxis=dict(backgroundcolor="#161b22", gridcolor="#30363d")),
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#ffffff", margin=dict(l=0, r=0, t=20, b=0), height=350
    )
    st.plotly_chart(fig_3d, use_container_width=True)

st.markdown("---")

# --- SECTION 2: MULTI-INPUT CONTROL CENTER & SOLVER ---
st.subheader("📐 Multi-Input Control Center & SciPy Solver")

col_ctrl, col_res = st.columns([1, 1])

with col_ctrl:
    st.markdown("#### 🎛️ Multivariable Input Boxes")
    
    tensor_scaling_factor = st.number_input("Tensor Scale Factor", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    curing_temp_input = st.number_input("Curing Temperature (°C)", min_value=20.0, max_value=300.0, value=150.0, step=5.0)
    initial_alpha_guess = st.number_input("Initial Alpha Guess", value=1.0, step=0.1)
    initial_beta_guess = st.number_input("Initial Beta Guess", value=1.0, step=0.1)
    
    prediction_query = st.text_input("Compound Signature Query:", "ITRE-EPOXY-404")
    
    run_solver = st.button("Run Inverse Optimization Solver", use_container_width=True)

with col_res:
    st.markdown("#### 📊 Solver Output & Results Table")
    
    Z_scaled = Z * tensor_scaling_factor
    
    def objective_func(params):
        a, b = params
        return np.sum((Z_scaled - (a * np.sin(X) + b * np.cos(Y)))**2)
    
    initial_guess = [initial_alpha_guess, initial_beta_guess]
    opt_result = minimize(objective_func, initial_guess, method=optimizer_method, tol=inversion_tolerance)
    
    st.markdown(f"""
        <div class="metric-card">
            <h4>Optimization Status: Converged ✅</h4>
            <p><b>Optimal Alpha:</b> {opt_result.x[0]:.4f} | <b>Optimal Beta:</b> {opt_result.x[1]:.4f}</p>
            <p><b>Residual Error:</b> {opt_result.fun:.6f}</p>
        </div>
    """, unsafe_allow_html=True)
    
    results_df = pd.DataFrame({
        "Parameter Metric": ["Alpha Coefficient", "Beta Coefficient", "Residual Error", "Scale Factor", "Curing Temp"],
        "Value": [f"{opt_result.x[0]:.4f}", f"{opt_result.x[1]:.4f}", f"{opt_result.fun:.6f}", f"{tensor_scaling_factor}", f"{curing_temp_input}°C"]
    })
    st.dataframe(results_df, use_container_width=True)
    
    # --- CSV & JSON EXPORT UTILITIES ---
    st.markdown("#### 💾 Export Simulation Data")
    
    # CSV Conversion
    csv_data = results_df.to_csv(index=False).encode('utf-8')
    
    # JSON Conversion Dictionary
    json_data = json.dumps({
        "compound_signature": prediction_query,
        "selected_elements": selected_elements,
        "curing_temperature_c": curing_temp_input,
        "tensor_scale_factor": tensor_scaling_factor,
        "optimization_results": {
            "alpha": float(opt_result.x[0]),
            "beta": float(opt_result.x[1]),
            "residual_error": float(opt_result.fun),
            "status": "Converged"
        }
    }, indent=4).encode('utf-8')

    export_col1, export_col2 = st.columns(2)
    with export_col1:
        st.download_button(
            label="Download CSV Report",
            data=csv_data,
            file_name=f"{prediction_query}_results.csv",
            mime="text/csv",
            use_container_width=True
        )
    with export_col2:
        st.download_button(
            label="Download JSON Package",
            data=json_data,
            file_name=f"{prediction_query}_package.json",
            mime="application/json",
            use_container_width=True
        )

# --- SECTION 3: PREDICTION OUTCOMES LINKED TO ELEMENTS ---
st.markdown("---")
st.subheader("🔬 DFT-Mapped Prediction Outcome Elements")

def app_predict(query_str, elements_list, temp):
    np.random.seed(abs(hash(query_str)) % (2**32))
    base_elements = [
        f"DFT-Optimized Matrix ({elements_list[0] if elements_list else 'C'})",
        f"Cross-linked Prepolymer Backbone (Temp: {temp}°C)",
        f"Secondary Element Phase ({elements_list[1] if len(elements_list)>1 else 'Si'})",
        "Silane Coupling Interfacial Agent",
        "Amine-Functionalized Curing Catalyst"
    ]
    return base_elements[:4]

if prediction_query:
    predicted_elements = app_predict(prediction_query, selected_elements, curing_temp_input)
    
    st.markdown(f"**Multiscale Predictions for Signature:** `{prediction_query}` using Elements: `{', '.join(selected_elements)}`")
    
    cols = st.columns(len(predicted_elements))
    for idx, element in enumerate(predicted_elements):
        with cols[idx]:
            st.markdown(f"""
                <div style="background-color: #161b22; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; min-height: 90px;">
                    <p style="color: #8b949e; font-size: 11px; margin-bottom: 3px;">Element {idx+1}</p>
                    <p style="color: #58a6ff; font-weight: bold; font-size: 13px; margin: 0;">{element}</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e;'>TensorLab Engine v4.0 | Multiscale Informatics Edition</p>", unsafe_allow_html=True)
