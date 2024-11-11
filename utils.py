import pandas as pd

def validate_columns(df, required_columns):
    """
    Checks if all required columns are present in the DataFrame.
    
    Parameters:
    - df (DataFrame): The DataFrame to check.
    - required_columns (list): List of column names that must be present.
    
    Returns:
    - bool: True if all required columns are present, False otherwise.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing required columns: {missing_columns}")
        return False
    return True

def format_currency(amount):
    """
    Formats a numeric amount into currency format (e.g., €1,000.00).
    
    Parameters:
    - amount (float): The amount to format.
    
    Returns:
    - str: Formatted currency string.
    """
    return f"€{amount:,.2f}"

def extract_month_year(df, date_column="Date"):
    """
    Adds 'Month' and 'Year' columns to a DataFrame based on a date column.
    
    Parameters:
    - df (DataFrame): The DataFrame with a date column.
    - date_column (str): The name of the date column to extract from.
    
    Returns:
    - DataFrame: The updated DataFrame with new 'Month' and 'Year' columns.
    """
    df[date_column] = pd.to_datetime(df[date_column])
    df["Month"] = df[date_column].dt.month
    df["Year"] = df[date_column].dt.year
    return df
