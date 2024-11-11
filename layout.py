# layout.py

import streamlit as st
import splash_screen
import loading_screen
import categorization
import chat_ui
import chart_ui
import expense_entry_form  # Import the form module
from utils import format_currency
from llm_chat import generate_chat_response
import pandas as pd
from create_goal_ui import display_goal_creation_ui

# Define the default categories (or get them from the model or settings)
default_categories = ["Food & Dining", "Utilities & Bills", "Transportation", 
                      "Entertainment", "Health & Wellness", "Income", "Miscellaneous"]

def render_sidebar():
    st.sidebar.header("Settings")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload your CSV", type="csv")
    
    # Category input
    st.sidebar.markdown("### Set General Categories")
    user_categories = st.sidebar.text_area(
        "Enter categories separated by commas:",
        value=", ".join(default_categories)
    )
    user_categories = [category.strip() for category in user_categories.split(",") if category.strip()]
    
    return uploaded_file, user_categories


def process_and_store_data(uploaded_file, user_categories):
    """Processes and categorizes data once, then stores it in session state."""
    if "categorized_data" not in st.session_state:
        # Use loading screen while processing
        df = loading_screen.process_data(uploaded_file)
        categories_df_all = categorization.process_transactions_in_batches(df, user_categories)
        categories_df_all = categorization.clean_transactions(categories_df_all)
        categorized_df = categorization.merge_categories(df, categories_df_all)
        
        # Store the categorized data in session state
        st.session_state["categorized_data"] = categorized_df


def render_main_content(uploaded_file, user_categories):
    """Main content area with tabs for Financial Goals, Categorized Transactions, and Financial Dashboard."""
    st.title("Moose")

    # Only process the data once when the file is uploaded
    if uploaded_file or "categorized_data" in st.session_state:
        # Process uploaded file if available, otherwise use session state data
        if uploaded_file:
            process_and_store_data(uploaded_file, user_categories)
        
        categorized_df = st.session_state["categorized_data"]  # Access the stored data

        # Create tabs for different sections
        tabs = st.tabs([ "Categorized Transactions",  "Financial Goals",  "Dashboard", 'Chat with Moose'])

        # Financial Goals Tab
        with tabs[0]:
            st.subheader("Categorized Transactions")
            # Date range picker
            min_date = pd.to_datetime(categorized_df["Date"]).min()
            max_date = pd.to_datetime(categorized_df["Date"]).max()
            
            start_date, end_date = st.date_input(
                "Date Range",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )

            # Filter data based on selected date range
            filtered_df = categorized_df[
                (pd.to_datetime(categorized_df["Date"]) >= pd.to_datetime(start_date)) & 
                (pd.to_datetime(categorized_df["Date"]) <= pd.to_datetime(end_date))
            ]

            st.write(filtered_df)  # Display the filtered categorized transactions





            
        # Categorized Transactions Tab
        with tabs[1]:
            st.subheader("Financial Goals")
            display_goal_creation_ui()  # Display goal creation and tracking UI

            

        # Financial Dashboard Tab
        with tabs[2]:
            st.subheader("Overall Summary")
            total_expense = categorized_df[categorized_df['Expense/Income'] == "Expense"]['Amount (EUR)'].sum()
            total_income = categorized_df[categorized_df['Expense/Income'] == "Income"]['Amount (EUR)'].sum()
            net_savings = total_income - total_expense

            st.metric("Total Expenses (€)", format_currency(total_expense))
            st.metric("Total Income (€)", format_currency(total_income))
            st.metric("Net Savings (€)", format_currency(net_savings))

            # Display charts using the filtered data
            st.header("Charts")
            chart_ui.render_chart_grid(filtered_df)

            

        with tabs[3]:
            # Chat UI Section
            st.header("Chat with Moose")
            chat_ui.render_chat_ui(filtered_df)


    else:
        # Show splash screen if no file is uploaded
        splash_screen.render_splash_screen()


def render_layout():
    """Renders the entire layout including the sidebar and main content."""
    uploaded_file, user_categories = render_sidebar()
    render_main_content(uploaded_file, user_categories)
    
    # Pass the user-defined categories to the expense entry form
    expense_entry_form.render_expense_entry_form(user_categories)

if __name__ == "__main__":
    render_layout()
