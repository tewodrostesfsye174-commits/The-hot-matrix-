# views/home_overview.py - Welcome Dashboard & Executive Summary
import streamlit as st
import pandas as pd
from math_engine import run_batch_simulation, generate_executive_report_html, verify_rbac_permission

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
                <span style="color: #8b949e; font-size: 10px; text-transform: uppercase; letter-spacing: 1.2px;">Welcome Dashboard &bull; Enterprise v2.6</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"<span style='color: #8b949e; font-size: 12px;'>Active Clearance Tier:</span> <span class='rbac-badge'>{st.session_state.get('user_role', 'Enterprise Admin')}</span>", unsafe_allow_html=True)
st.markdown("<hr style='margin: 12px 0; border-color: #30363d;'>", unsafe_allow_html=True)

st.markdown("#### 📊 Active Batch Simulation Queue")
st.markdown("<p style='color: #8b949e; font-size: 13px;'>Tracking persistent query sequences across live simulation nodes.</p>", unsafe_allow_html=True)

batch_df = run_batch_simulation(["SYNTH-BATCH-2comps-180C", "Al2O3-Beta", "Fe2O3-Gamma", "TiC-Delta"], 180.0, 2.0)
st.dataframe(batch_df, use_container_width=True)

if verify_rbac_permission(st.session_state.get('user_role', 'Enterprise Admin'), "reports"):
    st.markdown("---")
    st.markdown("#### 📑 Automated Executive Report Pipeline")
    report_html = generate_executive_report_html(
        st.session_state.get('user_role', 'Enterprise Admin'), "SYNTH-BATCH-2comps-180C", 180.0, 
        2.0, 1.15, 0.92, 0.001, batch_df
    )
    st.download_button(
        "📥 Download HTML Research Report", 
        data=report_html, 
        file_name="TensorLab_Executive_Report.html", 
        mime="text/html", 
        use_container_width=True
    )
