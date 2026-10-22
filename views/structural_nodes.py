# views/structural_nodes.py - Crystal Lattice Dynamics, DFT Quantum Node & Experimental Validation
import streamlit as st
import plotly.graph_objects as go
from math_engine import (
    generate_crystal_lattice_animation, 
    app_predict, 
    validate_experimental_results, 
    compute_dft_quantum_validation,
    run_monte_carlo_stress_test,
    verify_rbac_permission
)

def render():
    st.markdown("### ⚛️ Structural Nodes & Crystal Lattice Dynamics")
    st.markdown("<p style='color: #8b949e; font-size: 13px;'>Animate unit cell vibrations and inspect DFT-mapped atomic nodes.</p>", unsafe_allow_html=True)

    if verify_rbac_permission(st.session_state.get('user_role', 'Enterprise Admin'), "crystal_animation"):
        col_c1, col_c2 = st.columns([1, 3])
        with col_c1:
            lattice_system = st.selectbox("Lattice System", ["FCC (Face-Centered Cubic)", "BCC (Body-Centered Cubic)", "Diamond Cubic"], key="node_lattice")
            selected_code = lattice_system.split(" ")[0]
            thermal_slider = st.slider("Thermal Energy / Vibration", min_value=0.2, max_value=3.0, value=1.0, step=0.2, key="node_thermal")
            st.caption("Use the media player bar below the chart to play, pause, and scrub through thermal vibration frames.")
        
        with col_c2:
            base_coords, frames_data = generate_crystal_lattice_animation(lattice_type=selected_code, thermal_factor=thermal_slider)
            
            fig_crystal = go.Figure(
                data=[go.Scatter3d(
                    x=base_coords[:, 0], y=base_coords[:, 1], z=base_coords[:, 2],
                    mode='markers+text',
                    marker=dict(size=12, color=base_coords[:, 2], colorscale='Viridis', opacity=0.9),
                    text=[f"Atom {i+1}" for i in range(len(base_coords))],
                    textposition="top center"
                )],
                layout=go.Layout(
                    title=dict(text=f"3D Lattice Dynamics: {lattice_system}", font=dict(size=14)),
                    scene=dict(
                        xaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5]),
                        yaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5]),
                        zaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5])
                    ),
                    plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc",
                    margin=dict(l=0, r=0, t=40, b=60), height=440,
                    updatemenus=[dict(
                        type="buttons",
                        showactive=False,
                        x=0.5,
                        y=-0.18,
                        xanchor="center",
                        yanchor="top",
                        direction="left",
                        buttons=[
                            dict(label="▶ Play",
                                 method="animate",
                                 args=[None, {"frame": {"duration": 180, "redraw": True}, "fromcurrent": True, "transition": {"duration": 50}}]),
                            dict(label="❚❚ Pause",
                                 method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                        ]
                    )],
                    sliders=[dict(
                        active=0,
                        yanchor="top",
                        xanchor="left",
                        currentvalue={"prefix": "Frame: ", "font": {"color": "#58a6ff"}},
                        pad={"t": 35, "b": 10},
                        len=0.9,
                        x=0.05,
                        y=-0.1,
                        steps=[dict(args=[[str(k)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                                    label=str(k+1),
                                    method="animate") for k in range(len(frames_data))]
                    )]
                ),
                frames=[go.Frame(
                    data=[go.Scatter3d(
                        x=frame[:, 0], y=frame[:, 1], z=frame[:, 2],
                        mode='markers',
                        marker=dict(size=12, color=frame[:, 2], colorscale='Viridis', opacity=0.9)
                    )],
                    name=str(k)
                ) for k, frame in enumerate(frames_data)]
            )
            st.plotly_chart(fig_crystal, use_container_width=True)
    else:
        st.info("Crystalline lattice animation restricted for current clearance level.")

    st.markdown("---")
    st.markdown("#### ⚛️ Advanced DFT Quantum Outcome Examination")
    st.markdown("<p style='color: #8b949e; font-size: 13px;'>Inspect quantum mechanical properties including bandgap energy, electronic Density of States (DOS), and atomic forces.</p>", unsafe_allow_html=True)

    col_dft1, col_dft2 = st.columns(2)
    with col_dft1:
        dft_mat_select = st.selectbox("Select Crystal Material Node", ["Carbon Nanotube (CNT)", "Silicon Dioxide (SiO2)", "Aluminum Oxide (Al2O3)", "Lithium Iron Phosphate (LiFePO4)"], key="dft_mat")
    with col_dft2:
        dft_lattice_param = st.number_input("Lattice Spacing Parameter (Å)", min_value=1.0, max_value=10.0, value=3.84, step=0.05, key="dft_lat")

    if st.button("🧪 Execute DFT Quantum Analysis", use_container_width=True, key="btn_dft_exec"):
        dft_res = compute_dft_quantum_validation(dft_mat_select, dft_lattice_param)
        st.markdown(f"""
            <div style="background-color: #111625; border: 1px solid #30363d; border-left: 4px solid #58a6ff; padding: 14px; border-radius: 8px;">
                <span style="color: #58a6ff; font-weight: 700; font-size: 14px;">Status: {dft_res['dft_status']}</span><br>
                <span style="font-size: 13px; color: #f0f6fc;">
                    <b>Material Node:</b> {dft_res['material']} &bull; 
                    <b>Bandgap ($E_g$):</b> {dft_res['bandgap_ev']} eV
                </span><br>
                <span style="font-size: 12px; color: #8b949e;">
                    Peak Density of States (DOS): {dft_res['dos_peak_states']} states/eV &bull; 
                    Max Atomic Force: <b>{dft_res['atomic_force_ev_ang']} eV/Å</b>
                </span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔄 Repeated Stress-Testing & Monte Carlo Sensitivity Analysis")
    st.markdown("<p style='color: #8b949e; font-size: 13px;'>Run iterative stochastic stress tests across thermal and scale perturbation boundaries.</p>", unsafe_allow_html=True)

    col_mc1, col_mc2 = st.columns(2)
    with col_mc1:
        mc_base_temp = st.number_input("Base Curing Temperature (°C)", value=180.0, step=5.0, key="mc_temp")
    with col_mc2:
        mc_iterations = st.slider("Monte Carlo Iterations", min_value=10, max_value=200, value=50, step=10, key="mc_iter")

    if st.button("🚀 Run Monte Carlo Stress Test", use_container_width=True, key="btn_mc"):
        mc_df = run_monte_carlo_stress_test(mc_base_temp, 2.0, mc_iterations)
        st.dataframe(mc_df, use_container_width=True)
        st.download_button(
            "📥 Download Monte Carlo Stress Report (CSV)",
            data=mc_df.to_csv(index=False),
            file_name="TensorLab_MonteCarlo_Stress_Report.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("#### 🔬 Experimental vs. TensorLab / DFT Validation")
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    with col_ex1:
        exp_prop_name = st.selectbox("Material Property", ["Strength (MPa)", "Density (g/cm³)", "Bulk Modulus (GPa)", "Conductivity (S/cm)"], key="val_prop")
    with col_ex2:
        exp_measured = st.number_input("Experimental Lab Value", value=210.0, step=1.0, key="val_exp")
    with col_ex3:
        pred_modeled = st.number_input("TensorLab Predicted Value", value=200.0, step=1.0, key="val_pred")

    if st.button("⚖️ Run Validation & Error Analysis", use_container_width=True, key="btn_validate"):
        val_res = validate_experimental_results(exp_measured, pred_modeled, exp_prop_name)
        
        st.markdown(f"""
            <div class="config-card" style="border-left: 4px solid #238636;">
                <span style="color: #58a6ff; font-weight: 700;">Validation Status: {val_res['status']}</span><br>
                <span style="font-size: 13px; color: #f0f6fc;">
                    <b>Property:</b> {val_res['property']} &bull; 
                    <b>Experimental:</b> {val_res['experimental']} &bull; 
                    <b>Predicted:</b> {val_res['predicted']}
                </span><br>
                <span style="font-size: 12px; color: #8b949e;">
                    Absolute Error: {val_res['abs_error']} &bull; Percentage Deviation: <b>{val_res['pct_error']}%</b>
                </span>
            </div>
        """, unsafe_allow_html=True)
