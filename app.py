# app.py

import streamlit as st
import layout

def main():
    # Initialize session state if not already done

    
    if 'goal_created' not in st.session_state:
        st.session_state['goal_created'] = False

    layout.render_layout()

    # Reset the flag after rerun
    if st.session_state['goal_created']:
        st.session_state['goal_created'] = False

if __name__ == "__main__":
    main()

