# import streamlit as st
# import categorization
# import chat_ui
# import chart_ui
# from utils import format_currency
# from llm_chat import generate_chat_response
# from model import initialize_llm
# import pandas as pd

# def render_sidebar():
#     st.sidebar.header("Settings")
    
#     # File upload
#     uploaded_file = st.sidebar.file_uploader("Upload your CSV", type="csv")
    
#     # Category input
#     st.sidebar.markdown("### Set General Categories")
#     default_categories = ["Food & Dining", "Utilities & Bills", "Transportation", 
#                           "Entertainment", "Health & Wellness", "Income", "Miscellaneous"]
    
#     # User-editable category list
#     user_categories = st.sidebar.text_area(
#         "Enter categories separated by commas:",
#         value=", ".join(default_categories)
#     )
#     user_categories = [category.strip() for category in user_categories.split(",") if category.strip()]
    
#     return uploaded_file, user_categories


# def process_and_store_data(uploaded_file, user_categories):
#     """Processes and categorizes data once, then stores it in session state."""
#     if "categorized_data" not in st.session_state:
#         # Load, categorize, and store data in session state
#         df = categorization.load_data(uploaded_file)
#         categories_df_all = categorization.process_transactions_in_batches(df, user_categories)
#         categories_df_all = categorization.clean_transactions(categories_df_all)
#         categorized_df = categorization.merge_categories(df, categories_df_all)
        
#         # Store the categorized data in session state
#         st.session_state["categorized_data"] = categorized_df


# def render_main_content(uploaded_file, user_categories):
#     """Main content area displaying charts, metrics, and chat interface."""
#     st.title("Financial Dashboard")
    
#     # Only process the data once when the file is uploaded
#     if uploaded_file:
#         process_and_store_data(uploaded_file, user_categories)
#         categorized_df = st.session_state["categorized_data"]  # Access the stored data

#         # Date range picker
#         st.header("Select Date Range for Analysis")
#         min_date = pd.to_datetime(categorized_df["Date"]).min()
#         max_date = pd.to_datetime(categorized_df["Date"]).max()
        
#         start_date, end_date = st.date_input(
#             "Date Range",
#             value=[min_date, max_date],
#             min_value=min_date,
#             max_value=max_date
#         )

#         # Filter stored data based on the selected date range
#         filtered_df = categorized_df[
#             (pd.to_datetime(categorized_df["Date"]) >= pd.to_datetime(start_date)) & 
#             (pd.to_datetime(categorized_df["Date"]) <= pd.to_datetime(end_date))
#         ]

#         # Display categorized transactions
#         st.header("Categorized Transactions")
#         st.write(filtered_df)

#         # Display Overall Financial Metrics
#         st.header("Overall Summary")
#         total_expense = filtered_df[filtered_df['Expense/Income'] == "Expense"]['Amount (EUR)'].sum()
#         total_income = filtered_df[filtered_df['Expense/Income'] == "Income"]['Amount (EUR)'].sum()
#         net_savings = total_income - total_expense

#         st.metric("Total Expenses (€)", format_currency(total_expense))
#         st.metric("Total Income (€)", format_currency(total_income))
#         st.metric("Net Savings (€)", format_currency(net_savings))

#         # Display Charts in a 4x4 Grid Layout using filtered data
#         st.header("Charts")
#         chart_ui.render_chart_grid(filtered_df)

#         # Chat UI Section
#         st.header("Chat with Financial Assistant")
#         chat_ui.render_chat_ui(filtered_df)
#     else:
#         st.write("Please upload a CSV file to start.")


# def render_layout():
#     """Renders the entire layout including the sidebar and main content."""
#     uploaded_file, user_categories = render_sidebar()
#     render_main_content(uploaded_file, user_categories)



import streamlit as st
import categorization
import chat_ui
import chart_ui
from utils import format_currency
import pandas as pd

def render_sidebar():
    """Sidebar with file upload only."""
    st.sidebar.header("Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV", type="csv")
    return uploaded_file

def process_and_store_data(uploaded_file):
    """Processes and categorizes data once, then stores it in session state."""
    if "categorized_data" not in st.session_state:
        # Load, categorize, and store data in session state
        df = categorization.load_data(uploaded_file)
        general_categories = ["Food & Dining", "Utilities & Bills", "Transportation", 
                              "Entertainment", "Health & Wellness", "Income", "Miscellaneous"]
        categories_df_all = categorization.process_transactions_in_batches(df, general_categories)
        categories_df_all = categorization.clean_transactions(categories_df_all)
        categorized_df = categorization.merge_categories(df, categories_df_all)
        
        # Store the categorized data in session state
        st.session_state["categorized_data"] = categorized_df


def render_main_content(uploaded_file):
    """Main content area displaying charts, metrics, and chat interface."""
    st.title("Financial Dashboard")
    
    # Only process the data once when the file is uploaded
    if uploaded_file:
        process_and_store_data(uploaded_file)
        categorized_df = st.session_state["categorized_data"]  # Access the stored data

        # Date range picker
        st.header("Select Date Range for Analysis")
        min_date = pd.to_datetime(categorized_df["Date"]).min()
        max_date = pd.to_datetime(categorized_df["Date"]).max()
        
        start_date, end_date = st.date_input(
            "Date Range",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        # Filter stored data based on the selected date range
        filtered_df = categorized_df[
            (pd.to_datetime(categorized_df["Date"]) >= pd.to_datetime(start_date)) & 
            (pd.to_datetime(categorized_df["Date"]) <= pd.to_datetime(end_date))
        ]

        # Display categorized transactions
        st.header("Categorized Transactions")
        st.write(filtered_df)

        # Display Overall Financial Metrics
        st.header("Overall Summary")
        total_expense = filtered_df[filtered_df['Expense/Income'] == "Expense"]['Amount (EUR)'].sum()
        total_income = filtered_df[filtered_df['Expense/Income'] == "Income"]['Amount (EUR)'].sum()
        net_savings = total_income - total_expense

        st.metric("Total Expenses (€)", format_currency(total_expense))
        st.metric("Total Income (€)", format_currency(total_income))
        st.metric("Net Savings (€)", format_currency(net_savings))

        # Display Charts in a 4x4 Grid Layout using filtered data
        st.header("Charts")
        chart_ui.render_chart_grid(filtered_df)

        # Chat UI Section
        chat_ui.render_chat_ui(filtered_df)
    else:
        st.write("Please upload a CSV file to start.")

def render_layout():
    """Renders the entire layout including the sidebar and main content."""
    uploaded_file = render_sidebar()
    render_main_content(uploaded_file)
