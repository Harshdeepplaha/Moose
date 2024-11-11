# expense_entry_form.py

import streamlit as st
import pandas as pd
import categorization  # Import categorization functions

def render_expense_entry_form(categories):
    """
    Renders a form in the sidebar to allow the user to manually add new expenses or income.
    
    Parameters:
    - categories (list): A list of category names that the user can select from.
    """
    st.sidebar.markdown("### Add New Expense or Income")

    # Expense Entry Form
    with st.sidebar.form(key="expense_entry_form"):
        date = st.date_input("Date")
        description = st.text_input("Description")
        category = st.selectbox("Category", categories)  # Use provided categories
        amount = st.number_input("Amount (€)", min_value=0.0, step=1.0)
        expense_type = st.selectbox("Type", ["Expense", "Income"])
        
        # Submit button
        submit_button = st.form_submit_button(label="Add Entry")
    
    # Process form submission
    if submit_button:
        # Create a new entry DataFrame
        new_entry = pd.DataFrame({
            "Date": [date],
            "Name / Description": [description],
            "Expense/Income": [expense_type],
            "Amount (EUR)": [amount],
            "Category": [category]
        })
        
        # Append to the session-stored DataFrame if it exists
        if "categorized_data" in st.session_state:
            updated_df = pd.concat([st.session_state["categorized_data"], new_entry], ignore_index=True)
        else:
            updated_df = new_entry
        
        # Re-categorize the updated data (use batch processing if needed)
        user_categories = categories  # Use the categories passed in the function
        categories_df_all = categorization.process_transactions_in_batches(updated_df, user_categories)
        categories_df_all = categorization.clean_transactions(categories_df_all)
        categorized_df = categorization.merge_categories(updated_df, categories_df_all)
        
        # Update session state with the newly categorized data
        st.session_state["categorized_data"] = categorized_df
        st.session_state["data_updated"] = not st.session_state.get("data_updated", False)  # Toggle to refresh display

        # Display success message
        st.sidebar.success("Entry added successfully!")
