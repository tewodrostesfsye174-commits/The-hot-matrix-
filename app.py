# Securely fetching the admin password from Streamlit secrets
stored_admin_password = st.secrets.get("ADMIN_PASSWORD", "demo123")

if st.button("Authenticate", use_container_width=True):
    if password == stored_admin_password:
        st.session_state.authenticated = True
        st.session_state.user_role = selected_role
        st.rerun()
    else:
        st.error("Invalid access code.")
