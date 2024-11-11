# charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def time_series_line_chart(df):
    fig = px.line(df, x='Date', y='Amount (EUR)', color='Expense/Income',
                  title="Time Series of Income and Expenses")
    st.plotly_chart(fig)

def stacked_area_chart(df):
    fig = px.area(df, x="Date", y="Amount (EUR)", color="Expense/Income",
                  title="Cumulative Income and Expenses Over Time")
    st.plotly_chart(fig)

def category_bar_chart(df):
    fig = px.bar(df, x="Category", y="Amount (EUR)", color="Expense/Income",
                 title="Spending and Income by Category", barmode="group")
    st.plotly_chart(fig)

def pie_chart(df, expense_income_type):
    filtered_df = df[df['Expense/Income'] == expense_income_type]
    fig = px.pie(filtered_df, values="Amount (EUR)", names="Category", 
                 title=f"{expense_income_type} Distribution by Category")
    st.plotly_chart(fig)

def bubble_chart(df):
    fig = px.scatter(df, x="Date", y="Amount (EUR)", size="Amount (EUR)", color="Category",
                     title="Transaction Bubble Chart by Date and Category", hover_name="Category")
    st.plotly_chart(fig)

def monthly_breakdown_chart(df):
    df['Month'] = df['Date'].dt.to_period("M")
    monthly_data = df.groupby(['Month', 'Expense/Income'])['Amount (EUR)'].sum().unstack().fillna(0)
    monthly_data = monthly_data.reset_index()
    monthly_data['Month'] = monthly_data['Month'].dt.to_timestamp()

    fig = px.bar(monthly_data, x="Month", y=["Expense", "Income"], title="Monthly Income and Expenses",
                 barmode="group")
    st.plotly_chart(fig)

def cumulative_sum_line_chart(df):
    df = df.sort_values("Date")
    df['Cumulative Amount'] = df.groupby("Expense/Income")['Amount (EUR)'].cumsum()

    fig = px.line(df, x="Date", y="Cumulative Amount", color="Expense/Income",
                  title="Cumulative Income and Expenses Over Time")
    st.plotly_chart(fig)

def heatmap_transaction_frequency(df):
    df['Day of Week'] = df['Date'].dt.day_name()
    df['Hour of Day'] = df['Date'].dt.hour
    heatmap_data = df.groupby(['Day of Week', 'Hour of Day']).size().unstack(fill_value=0)

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis'
    ))
    fig.update_layout(title="Transaction Frequency Heatmap", xaxis_title="Hour of Day", yaxis_title="Day of Week")
    st.plotly_chart(fig)
