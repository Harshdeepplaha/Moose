# splash_screen.py

import streamlit as st

def render_splash_screen():
    """Displays a splash screen when no data is uploaded."""
    
    st.markdown("<h1 style='text-align: center; '>Your personal AI to track and manage your expenses!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; '>Please upload a CSV file or add an entry to start!</p>", unsafe_allow_html=True)
    
    st.image("splash3.png", use_container_width=False)
  # Replace with your splash image path
