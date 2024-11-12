import streamlit as st
import plotly.express as px
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



def time_series_line_chart(df):
    """
    Displays a time series line chart showing cumulative income, expenses, and net savings over time.
    """
    # Ensure Date column is in datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"])

    # Sort by date to ensure correct cumulative calculations
    df = df.sort_values("Date")

    # Separate income and expenses for cumulative calculations
    df["Cumulative Income"] = df[df["Expense/Income"] == "Income"]["Amount (EUR)"].cumsum().fillna(method="ffill")
    df["Cumulative Expense"] = df[df["Expense/Income"] == "Expense"]["Amount (EUR)"].cumsum().fillna(method="ffill")

    # Calculate net savings as the difference between cumulative income and expenses
    df["Net Savings"] = df["Cumulative Income"] - df["Cumulative Expense"]

    # Melt data for Plotly compatibility, using a unique `value_name`
    df_melted = pd.melt(
        df, 
        id_vars=["Date"], 
        value_vars=["Cumulative Income", "Cumulative Expense", "Net Savings"],
        var_name="Metric", 
        value_name="Value"  # Changed to "Value" to avoid conflicts
    )

    # Create the line chart
    fig = px.line(df_melted, x="Date", y="Value", color="Metric", 
                  title="Cumulative Income, Expenses, and Net Savings Over Time")

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





## only when prompted 





def plot_top_categories(result, title="Top Categories by Spending/Income"):
    """Display a bar chart for the top categories by spending or income using Plotly."""
    fig = px.bar(result, x=result.index, y=result.values, title=title, labels={"x": "Category", "y": "Amount (EUR)"})
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_monthly_growth(result, title="Monthly Growth Rate"):
    """Display a line chart for monthly growth rates using Plotly."""
    fig = px.line(result, x=result.index, y=result.values, title=title, labels={"x": "Month", "y": "Growth Rate (%)"})
    fig.update_traces(mode="markers+lines")  # Adds markers to the line chart
    return fig

def plot_yearly_summary(result):
    """Display a grouped bar chart for yearly summary of income, expenses, and net savings using Plotly."""
    fig = go.Figure()
    for col in result.columns:
        fig.add_trace(go.Bar(
            x=result.index,
            y=result[col],
            name=col
        ))
    fig.update_layout(
        title="Yearly Summary of Income, Expenses, and Net Savings",
        barmode='group',
        xaxis_title="Year",
        yaxis_title="Amount (EUR)"
    )
    return fig