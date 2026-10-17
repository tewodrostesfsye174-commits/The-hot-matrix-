import streamlit as st
from math_engine import verify_rbac_permission

# Page Configuration
st.set_page_config(
    page_title="TensorLab | Materials Informatics",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-Contrast Enterprise Theme Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f0f6fc; }
    h1, h2, h3, h4, h5, h6 { color: #58a6ff !important; font-weight: 700; }
    p, span, label, .stMarkdown, .stText { color: #f0f6fc !important; }
    .rbac-badge {
        background-color: #238636; color: #ffffff;
        padding: 4px 10px; border-radius: 4px;
        font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
    }
    .brand-container {
        background-color: #161b22; border: 1px solid #30363d;
        padding: 12px 16px; border-radius: 10px;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Universal st.session_state Initialization for State Persistence across Pages
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = "Junior Researcher"
if "query_sig" not in st.session_state:
    st.session_state.query_sig = "SYNTH-BATCH-2comps-180C"
if "curing_temp" not in st.session_state:
    st.session_state.curing_temp = 180.0
if "tensor_scale" not in st.session_state:
    st.session_state.tensor_scale = 1.46
if "chosen_reagents" not in st.session_state:
    st.session_state.chosen_reagents = ["Silicon Dioxide (SiO2)", "Carbon Nanotube (CNT)"]
if "flask_result" not in st.session_state:
    st.session_state.flask_result = {
        "status": "Initialized Workspace", "purity": 85.9, "density": 2.6, 
        "predicted_phase": "BCC Intermetallic Lattice", "derived_temp": 180.0, 
        "derived_scale": 1.46, "query_sig": "SYNTH-BATCH-2comps-180C"
    }

# Secure Authentication Gate
try:
    stored_admin_password = st.secrets.get("ADMIN_PASSWORD", "demo123")
except Exception:
    stored_admin_password = "demo123"

if not st.session_state.authenticated:
    st.markdown("<h3 style='text-align: center; color: #58a6ff;'>TensorLab Workspace Login</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 13px;'>Select your clearance role to access the enterprise platform.</p>", unsafe_allow_html=True)
    
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

# Master Brand Title Bar
st.markdown("""
    <div class="brand-container">
        <div>
            <h1 style="margin: 0; color: #58a6ff !important; font-size: 20px !important;">TENSOR<span style="color: #f0f6fc;">LAB</span></h1>
            <span style="color: #8b949e; font-size: 10px; text-transform: uppercase; letter-spacing: 1.2px;">Materials Informatics Sandbox &bull; v2.6 Enterprise</span>
        </div>
        <div>
            <span style="color: #8b949e; font-size: 11px;">Clearance:</span> <span class='rbac-badge'>{}</span>
        </div>
    </div>
""".format(st.session_state.user_role), unsafe_allow_html=True)

# Define Streamlit Multi-Page Navigation using st.navigation() and st.Page()
home_page = st.Page("views/home_overview.py", title="Home Overview", icon="🏠", default=True)
synthesis_page = st.Page("views/synthesis_lab.py", title="Virtual Synthesis Lab", icon="🧪")
solver_page = st.Page("views/solver_engine.py", title="Solver & Optimization Engine", icon="⚙️")
structural_page = st.Page("views/structural_nodes.py", title="Advanced Structural Nodes", icon="📐")

pg = st.navigation({
    "Workspace Navigation": [home_page, synthesis_page, solver_page, structural_page]
})

# Run the selected page router
pg.run()
