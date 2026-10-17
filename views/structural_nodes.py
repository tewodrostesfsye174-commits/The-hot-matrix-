# views/structural_nodes.py - Crystal Lattice Dynamics & DFT Mapped Nodes
import streamlit as st
import plotly.graph_objects as go
from math_engine import generate_crystal_lattice_animation, app_predict, verify_rbac_permission

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
st.markdown("#### DFT Mapped Element Nodes")
predicted_elements = app_predict("SYNTH-BATCH-2comps-180C", ["Carbon (C)", "Silicon (Si)", "Oxygen (O)"], 180.0)
cols = st.columns(len(predicted_elements))
for idx, element in enumerate(predicted_elements):
    with cols[idx]:
        st.markdown(f"""
            <div style="background-color: #111625; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; min-height: 80px;">
                <span style="color: #8b949e; font-size: 11px;">Node {idx+1}</span><br>
                <span style="color: #58a6ff; font-weight: 700; font-size: 12px;">{element}</span>
            </div>
        """, unsafe_allow_html=True)
