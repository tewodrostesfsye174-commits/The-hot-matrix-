import streamlit as st
import plotly.graph_objects as go
from math_engine import verify_rbac_permission, compute_elastic_tensor_matrix, run_inverse_design_screening, generate_crystal_lattice_animation, get_standard_reagents

st.markdown("### 📐 Advanced Structural & DFT Nodes")
st.markdown(f"<p style='color: #8b949e;'>Clearance Tier: <b>{st.session_state.user_role}</b></p>", unsafe_allow_html=True)

is_admin_or_senior = verify_rbac_permission(st.session_state.user_role, "inverse_design")
is_admin = verify_rbac_permission(st.session_state.user_role, "elastic_tensor")

# 1. DFT Mapped Element Nodes (Role Gated)
with st.container(border=True):
    st.markdown("#### ⚛️ DFT Mapped Element Nodes")
    if is_admin_or_senior:
        cols = st.columns(4)
        nodes = [
            f"DFT-Optimized Matrix ({st.session_state.query_sig})",
            f"Cross-linked Prepolymer (Temp:{st.session_state.curing_temp}°C)",
            "Secondary Element Phase (Silicon)",
            "Silane Coupling Interfacial Agent"
        ]
        for idx, node in enumerate(nodes):
            with cols[idx]:
                st.markdown(f"""
                    <div style="background-color: #111625; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; min-height: 80px;">
                        <span style="color: #8b949e; font-size: 11px;">Node {idx+1}</span><br>
                        <span style="color: #58a6ff; font-weight: 700; font-size: 12px;">{node}</span>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("DFT Node engineering is restricted to Senior Materials Scientists and Enterprise Admins.")

# 2. Elastic Tensor Matrix (Enterprise Admin Only)
with st.container(border=True):
    st.markdown("#### 📐 4th-Order Elastic Tensor Stiffness Matrix")
    if is_admin:
        elastic_data = compute_elastic_tensor_matrix(30, st.session_state.tensor_scale, st.session_state.curing_temp)
        el_cols = st.columns(len(elastic_data))
        for idx, (k_name, k_val) in enumerate(elastic_data.items()):
            with el_cols[idx]:
                st.markdown(f"""
                    <div style="background-color: #111625; border: 1px solid #30363d; padding: 10px; border-radius: 8px; text-align: center;">
                        <span style="color: #8b949e; font-size: 11px;">{k_name}</span><br>
                        <span style="color: #58a6ff; font-weight: 700; font-size: 14px;">{k_val}</span>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Elastic Tensor Stiffness Matrix computation is restricted to Enterprise Admins.")

# 3. Multi-Domain Inverse Design Search Cards
with st.container(border=True):
    st.markdown("#### 🔍 Multi-Domain Inverse Design & Reagent Screening")
    if is_admin_or_senior:
        with st.expander("⚙️ Mechanical Domain Targets", expanded=True):
            target_str_input = st.number_input("Target Strength (MPa)", min_value=50.0, max_value=350.0, value=200.0, step=10.0)
            target_den_input = st.number_input("Target Density (g/cm³)", min_value=1.0, max_value=5.0, value=2.5, step=0.1)

        with st.expander("🧪 Rheological & Fluid Domain Targets (Adhesives/Coatings)", expanded=False):
            target_visc_input = st.number_input("Target Viscosity (cP)", min_value=10.0, max_value=10000.0, value=1000.0, step=50.0)

        with st.expander("⚡ Electrochemical & Thermal Domain Targets", expanded=False):
            target_cond_input = st.number_input("Target Ionic Conductivity (S/cm)", min_value=0.0001, max_value=1.0, value=0.01, step=0.001)
            target_tg_input = st.number_input("Target Glass Transition Temp Tg (°C)", min_value=-50.0, max_value=300.0, value=80.0, step=5.0)

        if st.button("Screen 1,000+ Reagents via Multi-Domain Vector", use_container_width=True):
            targets_dict = {
                "strength": target_str_input, "density": target_den_input,
                "viscosity": target_visc_input, "conductivity": target_cond_input, "tg": target_tg_input
            }
            screening_df = run_inverse_design_screening(targets_dict, get_standard_reagents())
            st.dataframe(screening_df, use_container_width=True)
    else:
        st.info("Inverse design search modules restricted for current clearance tier.")

# 4. Crystal Lattice Physics & Thermal Vibration Animation
with st.container(border=True):
    st.markdown("#### 🧊 Crystalline Lattice Dynamics & Thermal Vibration")
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        lattice_system = st.selectbox("Lattice System", ["FCC (Face-Centered Cubic)", "BCC (Body-Centered Cubic)", "Diamond Cubic"])
        selected_code = lattice_system.split(" ")[0]
        thermal_slider = st.slider("Thermal Energy / Vibration Factor", min_value=0.2, max_value=3.0, value=1.0, step=0.2)
    with col_c2:
        base_coords, frames_data = generate_crystal_lattice_animation(lattice_type=selected_code, thermal_factor=thermal_slider)
        fig_crystal = go.Figure(
            data=[go.Scatter3d(
                x=base_coords[:, 0], y=base_coords[:, 1], z=base_coords[:, 2],
                mode='markers+text',
                marker=dict(size=10, color=base_coords[:, 2], colorscale='Viridis', opacity=0.9),
                text=[f"Atom {i+1}" for i in range(len(base_coords))], textposition="top center"
            )],
            layout=go.Layout(
                title=dict(text=f"3D Lattice Dynamics: {lattice_system}", font=dict(size=13)),
                scene=dict(
                    xaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5]),
                    yaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5]),
                    zaxis=dict(backgroundcolor="#111625", gridcolor="#30363d", range=[-0.5, 1.5])
                ),
                plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc",
                margin=dict(l=0, r=0, t=30, b=30), height=380,
                updatemenus=[dict(
                    type="buttons", showactive=False, x=0.5, y=-0.15, xanchor="center", yanchor="top", direction="left",
                    buttons=[
                        dict(label="▶ Play", method="animate", args=[None, {"frame": {"duration": 180, "redraw": True}, "fromcurrent": True}]),
                        dict(label="❚❚ Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
                    ]
                )]
            ),
            frames=[go.Frame(data=[go.Scatter3d(x=frame[:, 0], y=frame[:, 1], z=frame[:, 2], mode='markers', marker=dict(size=10, color=frame[:, 2], colorscale='Viridis'))], name=str(k)) for k, frame in enumerate(frames_data)]
        )
        st.plotly_chart(fig_crystal, use_container_width=True)
