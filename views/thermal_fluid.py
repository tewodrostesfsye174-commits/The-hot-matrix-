# views/thermal_fluid.py - Thermal Conductivity & Fluid Rheology Dynamics
import streamlit as st
from math_engine import run_thermal_fluid_simulation, verify_rbac_permission

st.markdown("### 🔥 Fluid Rheology & Thermal Conductivity Dynamics")
st.markdown("<p style='color: #8b949e; font-size: 13px;'>Simulate fluid flow regimes, thermal diffusion, and boundary layer stability for liquid resins and coatings.</p>", unsafe_allow_html=True)

if verify_rbac_permission(st.session_state.get('user_role', 'Enterprise Admin'), "advanced_solvers"):
    col_tf1, col_tf2, col_tf3 = st.columns(3)
    with col_tf1:
        visc_input = st.number_input("Dynamic Viscosity (cP)", min_value=0.1, max_value=50000.0, value=1250.0, step=50.0, key="tf_visc")
    with col_tf2:
        therm_cond_input = st.number_input("Thermal Conductivity (W/m·K)", min_value=0.01, max_value=500.0, value=1.45, step=0.05, key="tf_cond")
    with col_tf3:
        flow_rate_input = st.number_input("Fluid Flow Velocity (m/s)", min_value=0.001, max_value=10.0, value=0.25, step=0.01, key="tf_flow")

    if st.button("🌊 Run Thermal-Fluid Coupling Simulation", use_container_width=True, key="btn_tf"):
        tf_res = run_thermal_fluid_simulation(visc_input, therm_cond_input, flow_rate_input)
        
        st.markdown(f"""
            <div style="background-color: #111625; border: 1px solid #30363d; border-left: 4px solid #238636; padding: 14px; border-radius: 8px;">
                <span style="color: #58a6ff; font-weight: 700; font-size: 14px;">Status: {tf_res['status']}</span><br>
                <span style="font-size: 13px; color: #f0f6fc;">
                    <b>Flow Regime:</b> {tf_res['regime']} &bull; 
                    <b>Reynolds Number ($Re$):</b> {tf_res['reynolds']}
                </span><br>
                <span style="font-size: 12px; color: #8b949e;">
                    Thermal Diffusivity: <b>{tf_res['diffusivity']} m²/s</b>
                </span>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("Thermal-Fluid dynamics module restricted for current clearance level.")
