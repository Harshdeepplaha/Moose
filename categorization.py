import pandas as pd
from model import initialize_llm  # Import model initialization from model.py
from utils import validate_columns  # Import utility function for column validation

# Initialize the LLM instance once for reuse across categorization functions
llm = initialize_llm()

def load_data(uploaded_file):
    """Load transaction data from the uploaded CSV file and validate required columns."""
    df = pd.read_csv(uploaded_file)
    required_columns = ["Name / Description", "Amount (EUR)"]
    if not validate_columns(df, required_columns):
        raise ValueError(f"The uploaded file must contain the following columns: {required_columns}")
    return df

def save_data(df, file_path):
    """Saves the DataFrame to a specified CSV file."""
    df.to_csv(file_path, index=False)

def categorize_transactions(transaction_names, llm):
    """
    Categorize transactions using the LLM, restricted to predefined categories, with fallbacks for unmatched cases.
    """
    # Define the target general categories
    general_categories = [
        "Food & Dining", "Utilities & Bills", "Transportation", 
        "Entertainment", "Health & Wellness", "Income", "Miscellaneous"
    ]
    general_categories_str = ", ".join(general_categories)

    # Define the prompt with examples and constraints
    prompt = (
    "You are a financial assistant categorizing expenses. Please categorize each of the following transactions "
    "into ONE of the following exact general categories: "
    f"{general_categories_str}. Only use one of these categories, and if a transaction does not clearly fit, "
    "categorize it as 'Miscellaneous'. Do not create any new categories.\n\n"
    "Respond ONLY in the following strict format: 'Transaction - Category'. Do not include any extra information.\n\n"
    "Examples:\n"
    "1. Spotify AB by Adyen - Entertainment\n"
    "2. Uber Ride - Transportation\n"
    "3. Grocery Store - Food & Dining\n"
    "4. Doctor's Visit - Health & Wellness\n"
    "5. Rent Payment - Utilities & Bills\n"
    "6. Freelance Payment - Income\n\n"
    "Categorize the following transactions:\n"
    + transaction_names
)

    # Invoke the LLM with the prompt and log response for debugging
    response = llm.invoke(prompt)
    print("LLM Response:", response)  # Log the response to understand its format
    
    # Split the response by lines and filter for correctly formatted lines
    response_lines = response.split('\n')
    formatted_lines = [line for line in response_lines if ' - ' in line]

    # Warn if no valid responses are found
    if not formatted_lines:
        print("Warning: No valid 'Transaction - Category' lines found in LLM response.")
        return pd.DataFrame(columns=["Transaction", "Category"])

    # Convert formatted response into a DataFrame
    categories_df = pd.DataFrame({'Transaction vs category': formatted_lines})
    categories_df[['Transaction', 'Category']] = categories_df['Transaction vs category'].str.split(' - ', expand=True)

    # Ensure that only predefined categories are used; default to 'Miscellaneous' otherwise
    categories_df['Category'] = categories_df['Category'].apply(
        lambda x: x if x in general_categories else 'Miscellaneous'
    )

    # Fill any remaining null categories with 'Miscellaneous'
    categories_df['Category'].fillna('Miscellaneous', inplace=True)

    return categories_df[['Transaction', 'Category']]

def process_transactions_in_batches(df, categories, batch_size=10):
    """Batch process transactions for categorization."""
    unique_transactions = df["Name / Description"].unique()
    index_list = list(range(0, len(unique_transactions), batch_size)) + [len(unique_transactions)]
    categories_df_all = pd.DataFrame()

    # Loop through batches of transactions to categorize them
    for i in range(len(index_list) - 1):
        transaction_names = ','.join(unique_transactions[index_list[i]:index_list[i + 1]])
        try:
            categories_df = categorize_transactions(transaction_names, llm)
            # Only concatenate if the expected columns exist
            if not categories_df.empty and 'Transaction' in categories_df.columns:
                categories_df_all = pd.concat([categories_df_all, categories_df[['Transaction', 'Category']]], ignore_index=True)
            else:
                print(f"Warning: Batch {i} did not return valid 'Transaction' and 'Category' columns.")
        except Exception as e:
            print(f"Error during processing batch {i}: {e}")
            continue  # Skip the batch if there's an error

    return categories_df_all

def clean_transactions(df):
    """Clean the 'Transaction' column by removing unnecessary numbering or prefixes."""
    if 'Transaction' in df.columns:
        df['Transaction'] = df['Transaction'].str.replace(r'\d+\.\s+', '', regex=True)
    else:
        print("Warning: 'Transaction' column not found in the DataFrame for cleaning.")
    return df

def merge_categories(df, categories_df_all):
    """Merge categorized data with the original transaction data."""
    if 'Transaction' in categories_df_all.columns:
        merged_df = pd.merge(df, categories_df_all, left_on='Name / Description', right_on='Transaction', how='left')
    else:
        print("Warning: 'Transaction' column missing in categorized data; cannot merge.")
        merged_df = df.copy()  # Return original df if merge cannot be performed
    return merged_df

def main():
    general_categories = [
        "Food & Dining", "Utilities & Bills", "Transportation", 
        "Entertainment", "Health & Wellness", "Income", "Miscellaneous"
    ]
    
    # Load the transaction data
    df = load_data('transactions.csv')
    
    # Process transactions in batches and categorize them
    categories_df_all = process_transactions_in_batches(df, general_categories)
    
    # Clean and replace empty strings with NaN, then drop rows where 'Category' is NaN
    categories_df_all = clean_transactions(categories_df_all)
    categories_df_all.replace('', pd.NA, inplace=True)  # Replace empty strings with NaN
    categories_df_all.dropna(subset=['Category'], inplace=True)  # Drop rows with None or NaN in 'Category'
    
    # Merge categorized data with the original transaction data
    df = merge_categories(df, categories_df_all)
    
    # Save the results to a new CSV file
    save_data(df, 'categorized_transactions.csv')

if __name__ == "__main__":
    main()
