# splash_screen.py

import streamlit as st

def render_splash_screen():
    """Displays a splash screen when no data is uploaded."""
    
    st.markdown("<h2 style='text-align: center;'>Welcome to Your smart Financial Dashboard</h2>", unsafe_allow_html=True)
    st.write("Please upload a CSV file or add an entry to start.")
    st.image("splash2.png", use_container_width=True)
  # Replace with your splash image path
