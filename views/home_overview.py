import streamlit as st
from math_engine import run_batch_simulation, generate_executive_report_html, verify_rbac_permission

st.markdown("### 🏠 Welcome Dashboard")
st.markdown(f"<p style='color: #8b949e;'>Active Clearance Tier: <b>{st.session_state.user_role}</b></p>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("#### 📊 Active Batch Simulation Queue")
    st.markdown(f"<p style='font-size: 13px; color: #8b949e;'>Tracking persistent query sequence: <code>{st.session_state.query_sig}</code></p>", unsafe_allow_html=True)
    
    queries_list = [st.session_state.query_sig, "Al2O3-Beta", "Fe2O3-Gamma", "TiC-Delta"]
    batch_df = run_batch_simulation(queries_list, st.session_state.curing_temp, st.session_state.tensor_scale)
    st.dataframe(batch_df, use_container_width=True)

if verify_rbac_permission(st.session_state.user_role, "reports"):
    with st.container(border=True):
        st.markdown("#### 📥 Automated Executive Report Pipeline")
        report_html = generate_executive_report_html(
            st.session_state.user_role, st.session_state.query_sig, st.session_state.curing_temp, 
            st.session_state.tensor_scale, 1.07, 0.92, 0.0007, batch_df
        )
        st.download_button(
            "Download HTML Research Report", 
            data=report_html, 
            file_name=f"{st.session_state.query_sig}_research_report.html", 
            mime="text/html", 
            use_container_width=True
        )
else:
    st.info("Executive reporting download restricted to Enterprise Admins.")
