import streamlit as st
import pandas as pd
import charts  # Import your charts module
import chat_ui  # Import your chat UI module
from categorizer import process_transactions_in_batches, clean_transactions, merge_categories  # Import categorizer functions
from langchain_community.llms import Ollama  # Assuming this is the LLM you're using

# Sidebar UI for uploading transactions.csv file
st.sidebar.header("Upload Transactions File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Display default categories and allow the user to modify them
st.sidebar.header("Set General Categories")
default_categories = ["Food & Dining", "Utilities & Bills", "Transportation", 
                      "Entertainment", "Health & Wellness", "Income", "Miscellaneous"]

# Allow the user to edit the list of categories
user_categories = st.sidebar.text_area(
    "Enter categories separated by commas:",
    value=", ".join(default_categories)
)
user_categories = [category.strip() for category in user_categories.split(",") if category.strip()]

# If a file is uploaded, process it
if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Check if the necessary columns exist in the uploaded file
    if 'Name / Description' not in df.columns or 'Amount (EUR)' not in df.columns:
        st.error("The uploaded CSV file must contain 'Name / Description' and 'Amount (EUR)' columns.")
    else:
        # Initialize LLM
        llm = Ollama(model="llama3.2")

        # Process transactions with categorization
        categories_df_all = process_transactions_in_batches(df, llm, user_categories)

        # Clean the transaction names in the categorized data
        categories_df_all = clean_transactions(categories_df_all)

        # Merge the categorized data with the original transaction data
        categorized_df = merge_categories(df, categories_df_all)

        # Display the categorized transactions
        st.write("Categorized Transactions", categorized_df)

        # Display overall financial metrics
        st.header("Overall Summary")
        total_expense = categorized_df[categorized_df['Expense/Income'] == "Expense"]['Amount (EUR)'].sum()
        total_income = categorized_df[categorized_df['Expense/Income'] == "Income"]['Amount (EUR)'].sum()
        net_savings = total_income - total_expense

        st.metric("Total Expenses (€)", f"{total_expense:,.2f}")
        st.metric("Total Income (€)", f"{total_income:,.2f}")
        st.metric("Net Savings (€)", f"{net_savings:,.2f}")

        # Generate and display charts using categorized data
        st.header("Charts")
        st.subheader("Income and Expenses Over Time")
        charts.time_series_line_chart(categorized_df)

        st.subheader("Cumulative Income and Expenses Over Time")
        charts.stacked_area_chart(categorized_df)

        st.subheader("Spending and Income by Category")
        charts.category_bar_chart(categorized_df)

        st.subheader("Category Distribution for Expenses and Income")
        col1, col2 = st.columns(2)
        with col1:
            charts.pie_chart(categorized_df, "Expense")
        with col2:
            charts.pie_chart(categorized_df, "Income")

        st.subheader("Transaction Bubble Chart by Date and Category")
        charts.bubble_chart(categorized_df)

        st.subheader("Monthly Income and Expenses")
        charts.monthly_breakdown_chart(categorized_df)

        st.subheader("Cumulative Income and Expenses Over Time")
        charts.cumulative_sum_line_chart(categorized_df)

        st.subheader("Transaction Frequency Heatmap by Day and Time")
        charts.heatmap_transaction_frequency(categorized_df)

# Sidebar: Chatbot UI
chat_ui.chat_ui(df if 'df' in locals() else None)
