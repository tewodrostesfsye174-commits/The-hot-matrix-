import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math_engine import generate_tensor_grid, run_optimized_solver, run_pareto_optimization

st.markdown("### ⚙️ Solver & Optimization Engine")
st.markdown("<p style='color: #8b949e;'>Configure spatial tensor calculations, optimization routines, and multi-objective Pareto trade-offs.</p>", unsafe_allow_html=True)

with st.container(border=True):
    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        st.session_state.tensor_scale = st.number_input(
            "Tensor Scale Factor", min_value=0.1, max_value=10.0, 
            value=float(st.session_state.tensor_scale), step=0.1
        )
        initial_alpha = st.number_input("Initial Alpha Guess", value=1.0, step=0.1)
    with col_cfg2:
        curing_temp_input = st.number_input(
            "Curing Temperature (°C)", min_value=20.0, max_value=300.0, 
            value=float(st.session_state.curing_temp), step=5.0
        )
        initial_beta = st.number_input("Initial Beta Guess", value=1.0, step=0.1)

tensor_rank = 30
x_vals, y_vals, X, Y, Z = generate_tensor_grid(tensor_rank, st.session_state.tensor_scale, curing_temp_input)
weights, strengths, masses, efficiencies = run_pareto_optimization(tensor_rank, curing_temp_input)
opt_alpha, opt_beta, opt_residual = run_optimized_solver(Z, X, Y, "Nelder-Mead", 1e-4, initial_alpha, initial_beta)

with st.container(border=True):
    st.markdown("#### 📊 Execution Results & Pareto Trade-Offs")
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.markdown(f"<p style='color: #238636; font-weight: 700;'>Optimization Converged (Residual: {opt_residual:.6f})</p>", unsafe_allow_html=True)
        results_df = pd.DataFrame({
            "Parameter Metric": ["Alpha Coeff", "Beta Coeff", "Max Strength", "Min Mass/Cost"],
            "Value": [f"{opt_alpha:.4f}", f"{opt_beta:.4f}", f"{max(strengths):.2f} MPa", f"{min(masses):.2f} g/cm³"]
        })
        st.dataframe(results_df, use_container_width=True)
        
    with res_col2:
        st.caption("Pareto Frontier Efficiency Trade-Offs")
        fig_pareto = px.scatter(x=masses, y=strengths, color=efficiencies,
                                labels=dict(x="Mass / Cost", y="Strength (MPa)", color="Efficiency"),
                                color_continuous_scale="Turbo")
        fig_pareto.update_layout(plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=10, r=10, t=10, b=10), height=240)
        st.plotly_chart(fig_pareto, use_container_width=True)

with st.container(border=True):
    st.markdown("#### 🌐 3D Volumetric Topography")
    fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Plasma")])
    fig_3d.update_layout(
        scene=dict(xaxis=dict(backgroundcolor="#111625", gridcolor="#30363d"),
                   yaxis=dict(backgroundcolor="#111625", gridcolor="#30363d"),
                   zaxis=dict(backgroundcolor="#111625", gridcolor="#30363d")),
        plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=0, r=0, t=10, b=0), height=320
    )
    st.plotly_chart(fig_3d, use_container_width=True)
