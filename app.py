import streamlit as st

# This securely grabs the secret values from Streamlit Cloud's private vault
production_api_key = st.secrets["API_KEY"]
stored_admin_password = st.secrets["ADMIN_PASSWORD"]
