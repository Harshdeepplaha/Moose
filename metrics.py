import pandas as pd
import streamlit as st
import pandas as pd
from charts import plot_top_categories, plot_monthly_growth, plot_yearly_summary
# ... other imports if needed

from charts import (
    plot_top_categories, plot_monthly_growth, plot_yearly_summary, category_bar_chart,
    time_series_line_chart, stacked_area_chart, pie_chart, bubble_chart, monthly_breakdown_chart,
    cumulative_sum_line_chart, heatmap_transaction_frequency
)

def calculate_total_expenses(df):
    """Calculate total expenses from the categorized data."""
    return df[df["Expense/Income"] == "Expense"]["Amount (EUR)"].sum()

def calculate_total_income(df):
    """Calculate total income from the categorized data."""
    return df[df["Expense/Income"] == "Income"]["Amount (EUR)"].sum()

def calculate_net_savings(df):
    """Calculate net savings (total income - total expenses)."""
    total_income = calculate_total_income(df)
    total_expenses = calculate_total_expenses(df)
    return total_income - total_expenses

def calculate_category_spending(df, category):
    """Calculate total spending in a specified category."""
    category_expense = df[(df["Category"] == category) & (df["Expense/Income"] == "Expense")]
    return category_expense["Amount (EUR)"].sum()

def calculate_category_income(df, category):
    """Calculate total income in a specified category."""
    category_income = df[(df["Category"] == category) & (df["Expense/Income"] == "Income")]
    return category_income["Amount (EUR)"].sum()

def calculate_average_spending(df):
    """Calculate average spending across all expenses."""
    expenses = df[df["Expense/Income"] == "Expense"]
    return expenses["Amount (EUR)"].mean()

def calculate_max_spending(df):
    """Identify the maximum expense transaction."""
    expenses = df[df["Expense/Income"] == "Expense"]
    max_spending = expenses.loc[expenses["Amount (EUR)"].idxmax()]
    return max_spending["Name / Description"], max_spending["Amount (EUR)"]

def calculate_min_spending(df):
    """Identify the minimum expense transaction."""
    expenses = df[df["Expense/Income"] == "Expense"]
    min_spending = expenses.loc[expenses["Amount (EUR)"].idxmin()]
    return min_spending["Name / Description"], min_spending["Amount (EUR)"]

def calculate_monthly_expenses(df):
    """Calculate total expenses per month."""
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_expenses = df[df["Expense/Income"] == "Expense"].groupby("Month")["Amount (EUR)"].sum()
    return monthly_expenses

# Advanced metrics
def top_categories_by_spending(df, n=3):
    """Return the top N categories by spending."""
    expenses = df[df["Expense/Income"] == "Expense"]
    return expenses.groupby("Category")["Amount (EUR)"].sum().nlargest(n)

def top_categories_by_income(df, n=3):
    """Return the top N categories by income."""
    income = df[df["Expense/Income"] == "Income"]
    return income.groupby("Category")["Amount (EUR)"].sum().nlargest(n)

def monthly_growth_rate(df, type="Expense"):
    """Calculate the monthly growth rate for expenses or income."""
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_totals = df[df["Expense/Income"] == type].groupby("Month")["Amount (EUR)"].sum()
    growth_rate = monthly_totals.pct_change().fillna(0)
    return growth_rate

def category_budget_variance(df, budget_dict):
    """
    Compare actual spending against a budget for each category.
    - budget_dict: Dictionary with category as key and budget as value.
    """
    expenses = df[df["Expense/Income"] == "Expense"]
    actuals = expenses.groupby("Category")["Amount (EUR)"].sum()
    variance = actuals.subtract(pd.Series(budget_dict)).fillna(0)
    return variance

def savings_rate(df):
    """Calculate the savings rate as a percentage of total income."""
    total_income = calculate_total_income(df)
    total_expenses = calculate_total_expenses(df)
    return ((total_income - total_expenses) / total_income) * 100 if total_income > 0 else 0

def income_to_expense_ratio(df):
    """Calculate the ratio of income to expenses."""
    total_income = calculate_total_income(df)
    total_expenses = calculate_total_expenses(df)
    return total_income / total_expenses if total_expenses > 0 else np.inf

def spending_consistency(df):
    """Calculate the standard deviation of monthly spending as a measure of consistency."""
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_expenses = df[df["Expense/Income"] == "Expense"].groupby("Month")["Amount (EUR)"].sum()
    return monthly_expenses.std()

def yearly_summary(df):
    """Return total income and expenses aggregated by year."""
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    yearly_data = df.groupby(['Year', 'Expense/Income'])["Amount (EUR)"].sum().unstack(fill_value=0)
    yearly_data['Net Savings'] = yearly_data.get('Income', 0) - yearly_data.get('Expense', 0)
    return yearly_data

def recurring_expenses(df, threshold=3):
    """
    Identify recurring expenses based on transaction descriptions appearing at least `threshold` times.
    """
    expenses = df[df["Expense/Income"] == "Expense"]
    recurring = expenses["Name / Description"].value_counts()
    return recurring[recurring >= threshold]


# Natural language command mappings

# Update `command_map` to add plot functions for each metric
command_map = {
    "total expenses": (calculate_total_expenses, None),
    "total income": (calculate_total_income, None),
    "net savings": (calculate_net_savings, None),
    "top spending categories": (top_categories_by_spending, plot_top_categories),
    "top income categories": (top_categories_by_income, plot_top_categories),
    "monthly growth rate": (monthly_growth_rate, plot_monthly_growth),
    "budget variance": (category_budget_variance, category_bar_chart),
    "savings rate": (savings_rate, None),
    "income to expense ratio": (income_to_expense_ratio, None),
    "spending consistency": (spending_consistency, None),
    "yearly summary": (yearly_summary, plot_yearly_summary),
    "recurring expenses": (recurring_expenses, None),
    "average transaction size": (calculate_average_spending, None),
    "highest transaction": (calculate_max_spending, None),
    "lowest transaction": (calculate_min_spending, None),
    "monthly breakdown": (calculate_monthly_expenses, monthly_breakdown_chart),
    "yearly breakdown": (yearly_summary, plot_yearly_summary),
    "expense by category": (top_categories_by_spending, category_bar_chart),
    "income by category": (top_categories_by_income, category_bar_chart),
    "savings goal progress": (None, cumulative_sum_line_chart)  # Placeholder for custom goal progress function
}

def execute_command(command, df, **kwargs):
    """Execute the function associated with a command and return both metric result and plot function if available."""
    metric_func, plot_func = command_map.get(command, (None, None))
    if metric_func is None:
        return None, None
    result = metric_func(df, **kwargs)
    
    # Display the result
    st.write(result)
    
    # Display the plot if a plot function is available
    if plot_func is not None:
        fig = plot_func(result)
        st.plotly_chart(fig, use_container_width=True)
        
    return result, plot_func
