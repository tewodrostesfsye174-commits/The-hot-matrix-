# app.py - Master Router & Enterprise Shell for TensorLab
import streamlit as st

# Page Configuration for Mobile-First Enterprise View
st.set_page_config(
    page_title="TensorLab | Materials Informatics",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# High-Contrast Theme Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f0f6fc;
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
        padding: 16px;
        border-radius: 8px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    }
    .config-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .flask-card {
        background-color: #161b22;
        border: 2px dashed #58a6ff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    .api-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .rbac-badge {
        background-color: #238636;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: 1px solid #2ea043;
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
        padding: 16px 20px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .brand-title-box {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Secure Authentication Setup
try:
    stored_admin_password = st.secrets.get("ADMIN_PASSWORD", "demo123")
except Exception:
    stored_admin_password = "demo123"

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

# Define Multi-Page Structure using Streamlit Native Navigation
overview_page = st.Page("views/home_overview.py", title="Home Overview", icon="🏠")
synthesis_page = st.Page("views/synthesis_lab.py", title="Synthesis Lab", icon="🧪")
solver_page = st.Page("views/solver_engine.py", title="Solver Engine", icon="⚡")
nodes_page = st.Page("views/structural_nodes.py", title="Structural Nodes", icon="⚛️")

pg = st.navigation({
    "Core Modules": [overview_page, synthesis_page],
    "Advanced Analysis": [solver_page, nodes_page]
})

# Global Sidebar Enterprise Shell Controls
with st.sidebar:
    st.markdown("### 🔐 Enterprise Access")
    st.session_state["user_role"] = st.selectbox(
        "Clearance Tier",
        ["Junior Researcher", "Senior Materials Scientist", "Enterprise Admin"],
        index=2
    )
    
    st.divider()
    if st.button("🔒 Logout Session", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
        
    st.divider()
    st.caption("TensorLab v2.6 Enterprise Core • Mobile-First Engine")

# Run the selected page router
pg.run()
