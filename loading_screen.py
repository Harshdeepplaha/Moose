# loading_screen.py

import streamlit as st
import pandas as pd
import time

def process_data(file):
    """Processes uploaded CSV data with a loading screen."""
    with st.spinner("Processing data..."):
        # Simulate data processing time; replace this with actual processing logic.
        time.sleep(2)
        data = pd.read_csv(file)
        return data
