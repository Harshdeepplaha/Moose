import streamlit as st
import charts

def render_chart_grid(filtered_df):
    st.markdown("<h2>Financial Dashboard - Charts</h2>", unsafe_allow_html=True)
    
    # Create a 2x2 grid layout for the charts using st.columns
    col1, col2 = st.columns(2)

    # First row of charts
    with col1:
        with st.expander("Time Series Line Chart", expanded=True):
            charts.time_series_line_chart(filtered_df)
    
    with col2:
        with st.expander("Stacked Area Chart"):
            charts.stacked_area_chart(filtered_df)
    
    # Second row of charts
    with col1:
        with st.expander("Category-Based Bar Chart"):
            charts.category_bar_chart(filtered_df)
    
    with col2:
        with st.expander("Expense Distribution (Pie Chart)"):
            charts.pie_chart(filtered_df, type="Expense")
    
    # Add more rows or columns as needed for additional charts

