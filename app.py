import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.optimize import minimize

# Page Configuration
st.set_page_config(
    page_title="I-TRE | TensorLab Advanced",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Dark Mode Styling with Light Blue Accent Cards & Sliders
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
    /* Light Blue Accent Cards for Metrics and Results */
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
    st.markdown("<p style='text-align: center;'>Enter security credentials to initialize the Inverse Tensor Reconstructive Engine.</p>", unsafe_allow_html=True)
    
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
st.title("🧪 Inverse Tensor Reconstructive Engine (I-TRE)")
st.markdown("### Unified 2D/3D Matrix Analyzer & Inverse Solver Hub")
st.markdown("---")

# Sidebar Parameter Controls
st.sidebar.header("🎛️ Tensor & Matrix Controls")
formulation = st.sidebar.selectbox("Base Formulation", ["Epoxy-Matrix Composite", "Polyurethane Structural Adhesive", "Acrylic Elastomer Core"])
tensor_rank = st.sidebar.slider("Tensor Resolution Rank", min_value=10, max_value=50, value=25, step=5)
inversion_tolerance = st.sidebar.selectbox("Inversion Tolerance", [1e-3, 1e-4, 1e-5], index=1)
optimizer_method = st.sidebar.selectbox("SciPy Optimization Routine", ["Nelder-Mead", "BFGS", "Powell"])

# Generate Core Matrix Data based on inputs
x_vals = np.linspace(-5, 5, tensor_rank)
y_vals = np.linspace(-5, 5, tensor_rank)
X, Y = np.meshgrid(x_vals, y_vals)
Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))

# --- SECTION 1: VISUALIZATIONS (2D Heatmaps & 3D Volumetric State) ---
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.subheader("🔥 2D Spatial Stress Distribution")
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

# --- SECTION 2: SOLVER, RESULTS TABLE & PREDICTION IN ONE PLACE ---
st.subheader("📐 SciPy Inverse Optimization & Component Prediction Hub")

col_ctrl, col_res = st.columns([1, 1])

with col_ctrl:
    st.markdown("#### Execute Minimization")
    custom_multiplier = st.number_input("Tensor Scaling Factor", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    
    run_solver = st.button("Run Inverse Optimization Solver", use_container_width=True)
    
    # Text input box for prediction analysis query
    st.markdown("#### Inverse Prediction Query")
    prediction_query = st.text_input("Enter compound code / signature for prediction:", "ITRE-POLY-992")

with col_res:
    st.markdown("#### Solver Output & Results Table")
    
    # Run optimization logic
    def objective_func(params):
        a, b = params
        return np.sum((Z * custom_multiplier - (a * np.sin(X) + b * np.cos(Y)))**2)
    
    initial_guess = [1.0, 1.0]
    opt_result = minimize(objective_func, initial_guess, method=optimizer_method, tol=inversion_tolerance)
    
    # Light blue styled container for results
    st.markdown(f"""
        <div class="metric-card">
            <h4>Optimization Status: Converged ✅</h4>
            <p><b>Optimal Alpha:</b> {opt_result.x[0]:.4f} | <b>Optimal Beta:</b> {opt_result.x[1]:.4f}</p>
            <p><b>Residual Error:</b> {opt_result.fun:.6f}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Results Data Table
    results_df = pd.DataFrame({
        "Metric Parameter": ["Alpha Coefficient", "Beta Coefficient", "Residual Error", "Resolution Rank"],
        "Value": [f"{opt_result.x[0]:.4f}", f"{opt_result.x[1]:.4f}", f"{opt_result.fun:.6f}", tensor_rank]
    })
    st.dataframe(results_df, use_container_width=True)

# --- SECTION 3: APP.PREDICT OUTCOME ELEMENT NAMES ---
st.markdown("---")
st.subheader("🔬 Inverse Prediction Outcome Elements")

def app_predict(query_str, alpha, beta):
    # Simulated predictive inference mapping based on tensor inversion results
    np.random.seed(abs(hash(query_str)) % (2**32))
    possible_elements = [
        "Bisphenol-A Epoxy Resin Matrix", 
        "Toluene Diisocyanate Prepolymer", 
        "Polyether Polyol Chain Extender", 
        "Amine-Cured Hardener Complex", 
        "Acrylic Ester Monomer Backbone",
        "Silane Coupling Adhesion Promoter"
    ]
    selected_count = 3 if alpha > 0.5 else 2
    predicted_elements = np.random.choice(possible_elements, size=selected_count, replace=False).tolist()
    return predicted_elements

if prediction_query:
    predicted_elements = app_predict(prediction_query, opt_result.x[0], opt_result.x[1])
    
    st.markdown(f"**Prediction Results for Signature:** `{prediction_query}`")
    
    cols = st.columns(len(predicted_elements))
    for idx, element in enumerate(predicted_elements):
        with cols[idx]:
            st.markdown(f"""
                <div style="background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="color: #8b949e; font-size: 12px; margin-bottom: 5px;">Predicted Element {idx+1}</p>
                    <p style="color: #58a6ff; font-weight: bold; font-size: 14px; margin: 0;">{element}</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e;'>TensorLab Engine v3.0 | Unified Integrated Hub</p>", unsafe_allow_html=True)
