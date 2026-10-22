# app.py - Main Entry Point for TensorLab Enterprise Materials Platform
import streamlit as st
import os
import sys

# Ensure views directory is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Page Configuration
st.set_page_config(
    page_title="TensorLab | Enterprise Materials Informatics",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Dark-Theme Styling
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

# Sidebar Authentication & Navigation
st.sidebar.markdown("### 🔬 TENSORLAB")
st.sidebar.markdown("<p style='color: #8b949e; font-size: 12px;'>Enterprise Materials Informatics Platform v2.6</p>", unsafe_allow_html=True)

user_role = st.sidebar.selectbox(
    "Active Clearance Tier",
    ["Enterprise Admin", "Senior Materials Scientist", "Junior Researcher"],
    key="user_role"
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🧭 Navigation Menu")

page_selection = st.sidebar.radio(
    "Select View",
    ["Home Overview", "Synthesis Lab", "Solver Engine", "Structural Nodes", "Thermal & Fluid Dynamics"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
if st.sidebar.button("🔓 Logout Session"):
    st.sidebar.success("Session terminated safely.")

# Clean Isolated Page Routing (Prevents view overlapping)
if page_selection == "Home Overview":
    import views.home_overview as view_home
    view_home.render()

elif page_selection == "Synthesis Lab":
    import views.synthesis_lab as view_synth
    view_synth.render()

elif page_selection == "Solver Engine":
    import views.solver_engine as view_solver
    view_solver.render()

elif page_selection == "Structural Nodes":
    import views.structural_nodes as view_struct
    view_struct.render()

elif page_selection == "Thermal & Fluid Dynamics":
    import views.thermal_fluid as view_thermal
    view_thermal.render()
