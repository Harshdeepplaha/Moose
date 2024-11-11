import streamlit as st
import layout  # Imports the layout structure with sidebar and main content

# Main function to render the app layout
def main():
    # Set up Streamlit app configuration
    st.set_page_config(
        page_title="Financial Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Render the entire app layout
    layout.render_layout()

if __name__ == "__main__":
    main()
