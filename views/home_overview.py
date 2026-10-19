# views/home_overview.py - Welcome Dashboard & Executive Summary
import streamlit as st
import pandas as pd
from math_engine import run_batch_simulation, generate_executive_report_html, verify_rbac_permission

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f0f6fc; }
    .config-card {
        background-color: #111625;
        border: 1px solid #30363d;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 14px;
    }
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
    }
    .rbac-badge {
        background-color: #1f6feb;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
    }
    </style>
    <div class="brand-container">
        <div>
            <h1 style="margin: 0; color: #58a6ff !important; font-size: 22px !important; font-weight: 800; letter-spacing: 0.5px;">TENSOR<span style="color: #f0f6fc;">LAB</span></h1>
            <span style="color: #8b949e; font-size: 10px; text-transform: uppercase; letter-spacing: 1.2px;">Welcome Dashboard &bull; Enterprise v2.6</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"<span style='color: #8b949e; font-size: 12px;'>Active Clearance Tier: <span class='rbac-badge'>{st.session_state.get('user_role', 'Enterprise Admin')}</span></span>", unsafe_allow_html=True)
st.markdown("<hr style='margin: 12px 0; border-color: #30363d;'>", unsafe_allow_html=True)

st.markdown("#### 📊 Active Batch Simulation Queue")
st.markdown("<p style='color: #8b949e; font-size: 13px;'>Tracking persistent query sequences across live simulation nodes.</p>", unsafe_allow_html=True)

batch_df = run_batch_simulation(["SYNTH-BATCH-2comps-180C", "Al203-Beta-Scale-3"], 180.0, 2.0)
st.dataframe(batch_df, use_container_width=True)

if verify_rbac_permission(st.session_state.get('user_role', 'Enterprise Admin'), 'reports'):
    st.markdown("---")
    st.markdown("#### 📑 Automated Executive Report Pipeline")
    report_html = generate_executive_report_html(
        st.session_state.get('user_role', 'Enterprise Admin'), "SYNTH-BATCH-2comps-180C",
        180.0, 2.0, 1.15, 0.92, 0.001, batch_df
    )
    st.download_button(
        "📥 Download HTML Research Report",
        data=report_html,
        file_name="TensorLab_Executive_Report.html",
        mime="text/html",
        use_container_width=True
    )
