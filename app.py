# app.py - Main Multi-Page Streamlit Entry Point (Optimized for Mobile Performance)
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

# Main Multi-Page Navigation Selector using session state to prevent jitter
if "page_selection" not in st.session_state:
    st.session_state.page_selection = "Home Overview"

page_selection = st.sidebar.radio(
    "Select Module", 
    [
        "Home Overview", 
        "Synthesis Lab", 
        "Solver Engine", 
        "Structural Nodes", 
        "Thermal & Fluid Dynamics"
    ],
    label_visibility="collapsed",
    key="page_radio"
)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout Session", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Cached/Direct View Dispatcher Routing
@st.cache_resource
def load_view_module(module_name):
    if module_name == "Home Overview":
        import views.home_overview as mod
    elif module_name == "Synthesis Lab":
        import views.synthesis_lab as mod
    elif module_name == "Solver Engine":
        import views.solver_engine as mod
    elif module_name == "Structural Nodes":
        import views.structural_nodes as mod
    elif module_name == "Thermal & Fluid Dynamics":
        import views.thermal_fluid as mod
    else:
        import views.home_overview as mod
    return mod

# Render selected module cleanly
current_module = load_view_module(page_selection)
