# goal_manager.py

import pandas as pd

# Initialize an empty DataFrame for goals
goals_df = pd.DataFrame(columns=['Goal Name', 'Target Amount', 'Current Amount Saved', 'Target Date'])

def create_goal(goal_name, target_amount, target_date):
    """
    Adds a new goal to the goals DataFrame.
    
    Args:
        goal_name (str): The name of the goal.
        target_amount (float): The target amount for the goal.
        target_date (str): The target completion date for the goal (YYYY-MM-DD).
    
    Returns:
        pd.DataFrame: Updated DataFrame with the new goal added.
    """
    global goals_df
    new_goal = pd.DataFrame({
        'Goal Name': [goal_name],
        'Target Amount': [target_amount],
        'Current Amount Saved': [0.0],
        'Target Date': [target_date]
    })
    goals_df = pd.concat([goals_df, new_goal], ignore_index=True)
    return goals_df

def allocate_to_goal(goal_name, amount):
    """
    Allocates a specified amount to a goal.
    
    Args:
        goal_name (str): The name of the goal to allocate funds to.
        amount (float): The amount to allocate to the goal.
    
    Returns:
        pd.DataFrame: Updated DataFrame with the allocation added.
    """
    global goals_df
    if goal_name in goals_df['Goal Name'].values:
        goals_df.loc[goals_df['Goal Name'] == goal_name, 'Current Amount Saved'] += amount
        print(f"Allocated {amount} to {goal_name}.")
    else:
        print(f"Goal '{goal_name}' not found.")
    return goals_df

def track_goal_progress():
    """
    Calculates and displays the progress for each goal.
    
    Returns:
        pd.DataFrame: Updated DataFrame with progress percentage calculated.
    """
    global goals_df
    goals_df['Progress (%)'] = (goals_df['Current Amount Saved'] / goals_df['Target Amount']) * 100
    goals_df['Progress (%)'] = goals_df['Progress (%)'].clip(upper=100)  # Ensure progress doesn't exceed 100%
    return goals_df[['Goal Name', 'Target Amount', 'Current Amount Saved', 'Progress (%)', 'Target Date']]

def get_goals():
    """
    Returns the current goals DataFrame.
    
    Returns:
        pd.DataFrame: The DataFrame containing all goals.
    """
    return goals_df


def get_goal_details(goal_name):
    """Retrieve details for a specific goal."""
    global goals_df
    goal = goals_df[goals_df['Goal Name'] == goal_name]
    if goal.empty:
        return None
    return goal.iloc[0].to_dict()