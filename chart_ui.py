import streamlit as st
import charts

def render_chart_grid(filtered_df):
    st.markdown("<h2>Financial Dashboard - Charts</h2>", unsafe_allow_html=True)
    
    # Display charts within expanders, using filtered data
    with st.expander("Time Series Line Chart", expanded=True):
        charts.time_series_line_chart(filtered_df)
    
    with st.expander("Stacked Area Chart"):
        charts.stacked_area_chart(filtered_df)
    
    with st.expander("Category-Based Bar Chart"):
        charts.category_bar_chart(filtered_df)
    
    with st.expander("Expense Distribution (Pie Chart)"):
        charts.pie_chart(filtered_df, type="Expense")
    
    # Additional charts follow the same pattern
