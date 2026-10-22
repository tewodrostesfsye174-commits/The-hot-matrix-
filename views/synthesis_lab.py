# views/synthesis_lab.py - Virtual Synthesis & Inverse Design (Pillar 1 Upgraded & Expanded Domains)
import streamlit as st
import pandas as pd
from math_engine import get_standard_reagents, simulate_reagent_mixing, run_inverse_design_screening, verify_rbac_permission

def render():
    st.markdown("### 🧪 Virtual Synthesis Laboratory")
    st.markdown("<p style='color: #8b949e; font-size: 13px;'>Select standard chemical reagents from the shelf to drive the mathematical reaction chamber.</p>", unsafe_allow_html=True)

    col_shelf, col_flask = st.columns([1, 1])

    with col_shelf:
        st.markdown("##### 🗄️ Reagent Shelf (1,000+ Standard Chemicals)")
        available_shelf = get_standard_reagents()
        chosen_reagents = st.multiselect("Select Reagents for Synthesis", available_shelf, default=["Silicon Dioxide (SiO2)", "Carbon Nanotube (CNT)"], key="synth_reagents")
        synthesis_temp_input = st.slider("Flask Curing Temperature (°C)", min_value=20.0, max_value=300.0, value=180.0, step=5.0, key="synth_temp")

    with col_flask:
        st.markdown("##### ⚗️ Reaction Flask Chamber")
        if st.button("Mix & Initiate Synthesis Reaction", use_container_width=True, key="btn_mix"):
            st.session_state.flask_result = simulate_reagent_mixing(chosen_reagents, synthesis_temp_input)
        
        if "flask_result" not in st.session_state:
            st.session_state.flask_result = simulate_reagent_mixing(chosen_reagents, 180.0)
        
        res = st.session_state.flask_result
        st.markdown(f"""
            <div class="flask-card" style="border-left: 4px solid #58a6ff; background-color: #111625; padding: 14px; border-radius: 8px;">
                <span style="font-size: 26px;">🧪</span><br>
                <span style="color: #58a6ff; font-weight: 700; font-size: 14px;">Status: {res.get('status')}</span><br>
                <span style="font-size: 13px; color: #f0f6fc;">Predicted Phase: <b>{res.get('predicted_phase')}</b></span><br>
                <span style="font-size: 12px; color: #8b949e;">
                    <b>Thermodynamics:</b> $\\Delta H_f$: {res.get('enthalpy_formation')} kJ/mol &bull; $C_p$: {res.get('heat_capacity')} J/mol&middot;K<br>
                    <b>Mechanics:</b> Toughness: {res.get('fracture_toughness')} MPa&middot;m<sup>0.5</sup><br>
                    <b>Adhesives/Coatings:</b> Tension: {res.get('surface_tension')} mN/m &bull; Shrinkage: {res.get('cure_shrinkage')}% &bull; WVTR: {res.get('wvtr')} g/m²&middot;day<br>
                    <b>Batteries/Electronics:</b> Dielectric ($\\epsilon_r$): {res.get('dielectric_constant')} &bull; Bandgap: {res.get('bandgap_energy')} eV &bull; EC Window: {res.get('electrochemical_window')} V<br>
                    <b>General:</b> Purity: {res.get('purity')}% &bull; Density: {res.get('density')} g/cm³ &bull; Query: `{res.get('query_sig')}`
                </span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Multi-Domain Inverse Design & Reagent Screening")
    st.markdown("<p style='color: #8b949e; font-size: 13px;'>Expand domain categories below to configure multi-attribute property vectors for custom adhesives, batteries, or structural materials.</p>", unsafe_allow_html=True)

    if verify_rbac_permission(st.session_state.get('user_role', 'Enterprise Admin'), "inverse_design"):
        with st.expander("⚙️ Mechanical & Thermodynamic Domain Targets", expanded=True):
            col_t1, col_t2, col_t3 = st.columns(3)
            with col_t1:
                target_str_input = st.number_input("Target Strength (MPa)", min_value=1.0, max_value=2000.0, value=200.0, step=10.0)
            with col_t2:
                target_enth_input = st.number_input("Target Enthalpy ΔHf (kJ/mol)", min_value=-1000.0, max_value=0.0, value=-220.0, step=10.0)
            with col_t3:
                target_tough_input = st.number_input("Target Toughness (MPa·m^0.5)", min_value=0.5, max_value=50.0, value=4.5, step=0.5)

            target_den_input = st.number_input("Target Density (g/cm³)", min_value=0.1, max_value=50.0, value=2.5, step=0.1)

        with st.expander("🧪 Rheological & Fluid Domain Targets (Adhesives/Coatings)", expanded=False):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                target_visc_input = st.number_input("Target Viscosity (cP)", min_value=0.1, max_value=1000000.0, value=1000.0, step=50.0)
                target_shrink_input = st.number_input("Target Cure Shrinkage (%)", min_value=0.0, max_value=20.0, value=2.0, step=0.1)
            with col_a2:
                target_surf_input = st.number_input("Target Surface Tension (mN/m)", min_value=10.0, max_value=100.0, value=40.0, step=1.0)
                target_wvtr_input = st.number_input("Target WVTR (g/m²·day)", min_value=0.0, max_value=50.0, value=2.5, step=0.5)

        with st.expander("⚡ Electrochemical & Thermal Domain Targets (Batteries/Electronics)", expanded=False):
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                target_cond_input = st.number_input("Target Ionic Conductivity (S/cm)", min_value=0.0, max_value=10000.0, value=0.01, step=0.001)
                target_diel_input = st.number_input("Target Dielectric Constant (ε_r)", min_value=1.0, max_value=500.0, value=10.0, step=0.5)
            with col_b2:
                target_tg_input = st.number_input("Target Glass Transition Temp Tg (°C)", min_value=-273.0, max_value=2000.0, value=80.0, step=5.0)
                target_bg_input = st.number_input("Target Bandgap Energy (eV)", min_value=0.0, max_value=15.0, value=2.5, step=0.1)

        if st.button("🚀 Screen Reagents via Multi-Domain Vector", use_container_width=True, key="btn_screen"):
            targets_dict = {
                "strength": target_str_input, 
                "enthalpy": target_enth_input,
                "toughness": target_tough_input,
                "density": target_den_input,
                "viscosity": target_visc_input, 
                "surface_tension": target_surf_input,
                "cure_shrinkage": target_shrink_input,
                "conductivity": target_cond_input, 
                "dielectric": target_diel_input,
                "bandgap": target_bg_input,
                "tg": target_tg_input
            }
            screening_df = run_inverse_design_screening(targets_dict, available_shelf)
            st.dataframe(screening_df, use_container_width=True)
    else:
        st.info("Inverse design & multi-domain screening restricted for current clearance level.")
