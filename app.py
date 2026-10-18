# app.py - Main Multi-Page Streamlit Entry Point (Optimized Routing)
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="TensorLab | Materials Informatics Platform", 
    page_icon="🧪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Dark-Theme Styling Injection
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f0f6fc; }
    .sidebar .sidebar-content { background-color: #111625; }
    .config-card {
        background-color: #111625;
        border: 1px solid #30363d;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Import all view modules safely at the top level
from views import home_overview, synthesis_lab, solver_engine, structural_nodes, thermal_fluid

# Sidebar Authentication & Navigation Hub
st.sidebar.markdown("### 🔬 TENSORLAB")
st.sidebar.markdown("<p style='color: #8b949e; font-size: 12px;'>Enterprise Materials Informatics Platform v2.6</p>", unsafe_allow_html=True)

# Clearance Role State Management
user_role = st.sidebar.selectbox(
    "Active Clearance Tier", 
    ["Enterprise Admin", "Senior Materials Scientist", "Junior Researcher"],
    key="user_role"
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🧭 Navigation Menu")

# Main Multi-Page Navigation Selector
page_selection = st.sidebar.radio(
    "Select Module", 
    [
        "Home Overview", 
        "Synthesis Lab", 
        "Solver Engine", 
        "Structural Nodes", 
        "Thermal & Fluid Dynamics"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout Session", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Clean Page View Dispatcher Routing
if page_selection == "Home Overview":
    # home_overview logic renders here
    pass
elif page_selection == "Synthesis Lab":
    # synthesis_lab logic renders here
    pass
elif page_selection == "Solver Engine":
    # solver_engine logic renders here
    pass
elif page_selection == "Structural Nodes":
    # structural_nodes logic renders here
    pass
elif page_selection == "Thermal & Fluid Dynamics":
    # thermal_fluid logic renders here
    pass
