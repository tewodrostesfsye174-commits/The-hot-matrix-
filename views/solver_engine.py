# views/solver_engine.py - Tensor Grid Solvers, Pareto Optimization & Elastic Matrices
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math_engine import (
    generate_tensor_grid, 
    run_optimized_solver, 
    run_pareto_optimization, 
    compute_elastic_tensor_matrix,
    verify_rbac_permission
)

def render():
    st.markdown("### ⚡ Simulation Control Panel & Solver Engine")
    st.markdown("<p style='color: #8b949e; font-size: 13px;'>Configure spatial scaling, tensor ranks, and execute advanced multi-objective optimization solvers.</p>", unsafe_allow_html=True)

    col_ctrl, col_res = st.columns([1, 1])

    with col_ctrl:
        tensor_scaling_factor = st.number_input("Tensor Scale Factor", min_value=0.1, max_value=10.0, value=2.0, step=0.1, key="sol_scale")
        curing_temp_input = st.number_input("Curing Temperature (°C)", min_value=20.0, max_value=300.0, value=180.0, step=5.0, key="sol_temp")
        initial_alpha_guess = st.number_input("Initial Alpha Guess", value=1.0, step=0.1, key="sol_alpha")
        initial_beta_guess = st.number_input("Initial Beta Guess", value=1.0, step=0.1, key="sol_beta")
        tensor_rank = 30
        optimizer_method = "Nelder-Mead"
        inversion_tolerance = 1e-4

    x_vals, y_vals, X, Y, Z = generate_tensor_grid(tensor_rank, tensor_scaling_factor, curing_temp_input)
    weights, strengths, masses, efficiencies = run_pareto_optimization(tensor_rank, curing_temp_input)
    opt_alpha, opt_beta, opt_residual = run_optimized_solver(Z, X, Y, optimizer_method, inversion_tolerance, initial_alpha_guess, initial_beta_guess)

    with col_res:
        st.markdown("#### Execution Results & Metrics")
        st.markdown(f"""
            <div style="background-color: #111625; border: 1px solid #30363d; padding: 16px; border-radius: 10px; margin-bottom: 14px;">
                <div style="font-weight: 700; margin-bottom: 4px; font-size: 14px;">Optimization Converged</div>
                <div style="font-size: 13px; color: #f0f6fc;">Max Efficiency: {max(efficiencies):.4f} &bull; Residual: {opt_residual:.6f}</div>
            </div>
        """, unsafe_allow_html=True)
        
        results_df = pd.DataFrame({
            "Parameter Metric": ["Alpha Coefficient", "Beta Coefficient", "Max Strength Score", "Min Mass/Cost Score", "Curing Temp"],
            "Value": [f"{opt_alpha:.4f}", f"{opt_beta:.4f}", f"{max(strengths):.2f} MPa", f"{min(masses):.2f} g/cm³", f"{curing_temp_input}°C"]
        })
        st.dataframe(results_df, use_container_width=True)

    if verify_rbac_permission(st.session_state.get('user_role', 'Enterprise Admin'), "elastic_tensor"):
        st.markdown("---")
        st.markdown("#### 📐 Elastic Tensor Stiffness Matrix & Mechanical Moduli")
        elastic_data = compute_elastic_tensor_matrix(tensor_rank, tensor_scaling_factor, curing_temp_input)
        el_cols = st.columns(len(elastic_data))
        for idx, (k_name, k_val) in enumerate(elastic_data.items()):
            with el_cols[idx]:
                st.markdown(f"""
                    <div style="background-color: #111625; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center;">
                        <span style="color: #8b949e; font-size: 11px;">{k_name}</span><br>
                        <span style="color: #58a6ff; font-weight: 700; font-size: 15px;">{k_val}</span>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Spatial & Multi-Objective Visualizations")
    col_v1, col_v2, col_v3 = st.columns(3)

    with col_v1:
        st.caption("2D Spatial Stress")
        fig_2d = px.imshow(Z, x=x_vals, y=y_vals, color_continuous_scale="Viridis")
        fig_2d.update_layout(plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=10, r=10, t=10, b=10), height=280)
        st.plotly_chart(fig_2d, use_container_width=True)

    with col_v2:
        st.caption("3D Volumetric State")
        fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Plasma")])
        fig_3d.update_layout(
            scene=dict(xaxis=dict(backgroundcolor="#111625", gridcolor="#30363d"),
                       yaxis=dict(backgroundcolor="#111625", gridcolor="#30363d"),
                       zaxis=dict(backgroundcolor="#111625", gridcolor="#30363d")),
            plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=0, r=0, t=10, b=0), height=280
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_v3:
        st.caption("Pareto Frontier Trade-Offs")
        fig_pareto = px.scatter(x=masses, y=strengths, color=efficiencies,
                                labels=dict(x="Mass / Cost", y="Strength (MPa)", color="Efficiency"),
                                color_continuous_scale="Turbo")
        fig_pareto.update_layout(plot_bgcolor="#0b0f19", paper_bgcolor="#0b0f19", font_color="#f0f6fc", margin=dict(l=10, r=10, t=10, b=10), height=280)
        st.plotly_chart(fig_pareto, use_container_width=True)
