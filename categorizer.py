import pandas as pd
from langchain_community.llms import Ollama  # Assuming this is the LLM you're using
import multiprocessing


def load_data(file_path):
    """Loads the transaction data from a CSV file."""
    return pd.read_csv(file_path)


def save_data(df, file_path):
    """Saves the dataframe to a CSV file."""
    df.to_csv(file_path, index=False)


def categorize_transactions(transaction_names, llm, general_categories):
    """Categorizes transactions using LLM and a list of general categories."""
    general_categories_str = ", ".join(general_categories)
    
    prompt = (
        "Please categorize the following expenses into one of the following general categories: "
        f"{general_categories_str}. If the category doesn't fit, categorize it as 'Miscellaneous'. "
        "For example: Spotify AB by Adyen - Entertainment, Beta Boulders Ams Amsterdam Nld - Sports, etc.\n"
        + transaction_names
    )
    
    # Invoke the LLM with the prompt
    response = llm.invoke(prompt)
    
    # Process LLM's response
    response_lines = response.split('\n')
    formatted_lines = [line for line in response_lines if ' - ' in line]
    
    # Create dataframe from categorized data
    categories_df = pd.DataFrame({'Transaction vs category': formatted_lines})
    categories_df[['Transaction', 'Category']] = categories_df['Transaction vs category'].str.split(' - ', expand=True)

    return categories_df


def process_transactions_in_batches(df, llm, general_categories, batch_size=30):
    """Processes transactions in batches for better performance."""
    unique_transactions = df["Name / Description"].unique()
    
    index_list = list(hop(0, len(unique_transactions), batch_size))
    categories_df_all = pd.DataFrame()
    
    # Process each batch
    for i in range(0, len(index_list)-1):
        transaction_names = unique_transactions[index_list[i]:index_list[i+1]]
        transaction_names = ','.join(transaction_names)
        
        # Categorize transactions in the batch
        try:
            categories_df = categorize_transactions(transaction_names, llm, general_categories)
            categories_df_all = pd.concat([categories_df_all, categories_df[['Transaction', 'Category']]], ignore_index=True)
        except Exception as e:
            print(f"Error during processing batch {i}: {e}")
            continue  # Skip this batch if there's an issue

    return categories_df_all


def hop(start, stop, step):
    """Generates indices for batch processing."""
    for i in range(start, stop, step):
        yield i
    yield stop


def clean_transactions(df):
    """Cleans the 'Transaction' column by removing unnecessary numbering."""
    df['Transaction'] = df['Transaction'].str.replace(r'\d+\.\s+', '', regex=True)
    return df


def merge_categories(df, categories_df_all):
    """Merges the categorized data with the original transaction data."""
    df = pd.merge(df, categories_df_all, left_on='Name / Description', right_on='Transaction', how='left')
    return df


def main():
    # Define the general categories
    general_categories = [
        "Food & Dining", "Utilities & Bills", "Transportation", 
        "Entertainment", "Health & Wellness", "Income", "Miscellaneous"
    ]
    
    # Load transaction data
    df = load_data('transactions.csv')

    # Process transactions in batches
    llm = Ollama(model="llama3.2")  # Initialize the LLM
    categories_df_all = process_transactions_in_batches(df, llm, general_categories)

    # Clean the 'Transaction' column
    categories_df_all = clean_transactions(categories_df_all)

    # Merge categorized data with original dataframe
    df = merge_categories(df, categories_df_all)

    # Save the results to a new CSV
    save_data(df, 'categorized_transactions.csv')


if __name__ == "__main__":
    main()
