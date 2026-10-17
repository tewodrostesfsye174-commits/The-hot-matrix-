import streamlit as st
from math_engine import get_standard_reagents, simulate_reagent_mixing

st.markdown("### 🧪 Virtual Synthesis Laboratory")
st.markdown("<p style='color: #8b949e;'>Formulate mixtures from 1,000+ standard reagents and evaluate reaction parameters.</p>", unsafe_allow_html=True)

available_shelf = get_standard_reagents()

with st.container(border=True):
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        st.session_state.chosen_reagents = st.multiselect(
            "Select Reagents for Synthesis", 
            available_shelf, 
            default=st.session_state.chosen_reagents
        )
    with col_ctrl2:
        st.session_state.curing_temp = st.slider(
            "Flask Curing Temperature (°C)", 
            min_value=20.0, max_value=300.0, 
            value=float(st.session_state.curing_temp), step=5.0
        )

    if st.button("Mix & Initiate Synthesis Reaction", use_container_width=True):
        st.session_state.flask_result = simulate_reagent_mixing(st.session_state.chosen_reagents, st.session_state.curing_temp)
        st.session_state.query_sig = st.session_state.flask_result.get("query_sig")
        st.session_state.tensor_scale = st.session_state.flask_result.get("derived_scale")
        st.success("Reaction successfully calculated and synchronized to session state!")

res = st.session_state.flask_result

with st.container(border=True):
    st.markdown("#### ⚗️ Reaction Chamber Metrics")
    st.markdown(f"<p style='color: #58a6ff; font-weight: 700;'>Status: {res.get('status')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 13px;'>Predicted Phase: <b>{res.get('predicted_phase')}</b> &bull; Query Signature: <code>{res.get('query_sig')}</code></p>", unsafe_allow_html=True)
    
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        st.metric(label="Compound Purity", value=f"{res.get('purity')}%", delta="+1.2%")
    with mcol2:
        st.metric(label="Compound Density", value=f"{res.get('density')} g/cm³", delta="-0.1 g/cm³")
