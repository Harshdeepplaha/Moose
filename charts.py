import streamlit as st
import plotly.express as px
import pandas as pd

def time_series_line_chart(df):
    """
    Displays a time series line chart of income and expenses over time.
    """
    fig = px.line(df, x="Date", y="Amount (EUR)", color="Expense/Income", 
                  title="Income and Expenses Over Time")
    st.plotly_chart(fig, use_container_width=True)

def stacked_area_chart(df):
    """
    Displays a stacked area chart to show cumulative income and expenses over time.
    """
    fig = px.area(df, x="Date", y="Amount (EUR)", color="Expense/Income", 
                  title="Cumulative Income and Expenses Over Time")
    st.plotly_chart(fig, use_container_width=True)

def category_bar_chart(df):
    """
    Displays a bar chart comparing spending across categories.
    """
    fig = px.bar(df, x="Category", y="Amount (EUR)", color="Expense/Income", 
                 title="Spending and Income by Category")
    st.plotly_chart(fig, use_container_width=True)

def pie_chart(df, type="Expense"):
    """
    Displays a pie chart showing the proportion of each category for expenses or income.
    
    Parameters:
    - type (str): "Expense" or "Income" to filter by type.
    """
    filtered_df = df[df["Expense/Income"] == type]
    fig = px.pie(filtered_df, names="Category", values="Amount (EUR)", 
                 title=f"{type} Distribution by Category")
    st.plotly_chart(fig, use_container_width=True)

def bubble_chart(df):
    """
    Displays a bubble chart of transactions, with size representing transaction amount.
    """
    fig = px.scatter(df, x="Date", y="Amount (EUR)", size="Amount (EUR)", color="Category", 
                     title="Bubble Chart of Transactions Over Time")
    st.plotly_chart(fig, use_container_width=True)

def monthly_breakdown_chart(df):
    """
    Displays a grouped bar chart showing income and expenses by month.
    """
    # Extract month and year for grouping
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")
    monthly_df = df.groupby(["Month", "Expense/Income"])["Amount (EUR)"].sum().reset_index()
    
    fig = px.bar(monthly_df, x="Month", y="Amount (EUR)", color="Expense/Income", barmode="group", 
                 title="Monthly Income and Expenses Breakdown")
    st.plotly_chart(fig, use_container_width=True)

def cumulative_sum_line_chart(df):
    """
    Displays a cumulative sum line chart of spending and income over time.
    """
    df = df.sort_values("Date")  # Ensure data is sorted by date
    df["Cumulative Sum"] = df["Amount (EUR)"].cumsum()
    fig = px.line(df, x="Date", y="Cumulative Sum", title="Cumulative Balance Over Time")
    st.plotly_chart(fig, use_container_width=True)

def heatmap_transaction_frequency(df):
    """
    Displays a heatmap for transaction frequency by day of the week and time of day.
    """
    # Example of creating a heatmap by assuming 'Day' and 'Time' columns exist in df
    df['Day'] = pd.to_datetime(df["Date"]).dt.day_name()
    df['Time'] = pd.to_datetime(df["Date"]).dt.hour
    frequency_df = df.groupby(['Day', 'Time']).size().reset_index(name="Frequency")
    
    fig = px.density_heatmap(frequency_df, x="Time", y="Day", z="Frequency", 
                             title="Transaction Frequency by Day and Time", nbinsx=24)
    st.plotly_chart(fig, use_container_width=True)
