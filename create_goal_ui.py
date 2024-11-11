# create_goal_ui.py

import streamlit as st
import goal_manager as gm
import plotly.graph_objects as go
import itertools

def chunks(iterable, n):
    """Yield successive n-sized chunks from an iterable."""
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            break
        yield chunk

def display_goal_rings():
    """
    Display each goal as a ring chart to visualize progress horizontally.
    """
    goals_df = gm.track_goal_progress()  # Get goals with updated progress
    
    # Check if there are goals to display
    if goals_df.empty:
        st.write("No goals available. Please create a goal first.")
        return
    
    # Define how many rings per row
    rings_per_row = 3
    
    # Split goals into chunks using the updated chunks function
    goal_chunks = list(chunks(goals_df.iterrows(), rings_per_row))
    
    for chunk in goal_chunks:
        cols = st.columns(len(chunk))  # Dynamically set the number of columns based on the chunk size
        for idx, (i, row) in enumerate(chunk):
            goal_name = row['Goal Name']
            target_amount = row['Target Amount']
            current_amount = row['Current Amount Saved']
            progress = row['Progress (%)']
            
            # Create a ring chart using Plotly
            fig = go.Figure(go.Pie(
                values=[progress, 100 - progress],
                labels=['Progress', 'Remaining'],
                marker=dict(colors=['#4CAF50', '#e0e0e0']),
                hole=0.7,  # Creates the "donut" shape
                textinfo='none'
            ))

            # Update layout to display as a ring
            fig.update_layout(
                title=f"{goal_name}",
                annotations=[dict(text=f"{progress:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)],
                showlegend=False,
                width=250,
                height=250,
                margin=dict(l=20, r=20, t=40, b=20)
            )

            # Display the chart in the corresponding column
            cols[idx].plotly_chart(fig, use_container_width=True)

def display_goal_creation_ui():
    """
    Displays the UI for creating a new goal and allocating money to an existing goal within a dropdown menu.
    """
    st.write("## Financial Goals")
    
    # Display goals and progress as rings within an expander
    with st.expander("View Goals and Progress"):
        display_goal_rings()
    
    # Use an expander for the goal creation and allocation UI
    with st.expander("Manage Goals"):
        # Arrange goal creation and allocation forms side by side
        col1, col2 = st.columns(2)

        # Goal creation form in the first column
        with col1:
            st.write("### Create a New Goal")
            goal_name = st.text_input("Goal Name", key="goal_name")
            target_amount = st.number_input("Target Amount (EUR)", min_value=0.0, key="target_amount")
            target_date = st.date_input("Target Date", key="target_date")
            
            if st.button("Add Goal", key="add_goal_button"):
                if goal_name and target_amount > 0:
                    gm.create_goal(goal_name, target_amount, target_date.strftime("%Y-%m-%d"))
                    st.success(f"Goal '{goal_name}' created!")
                    st.session_state["goal_created"] = True  # Trigger a rerun
                else:
                    st.error("Please enter a valid goal name and target amount.")
        
        # Goal allocation form in the second column
        with col2:
            st.write("### Allocate Money to a Goal")
            if not gm.get_goals().empty:
                selected_goal = st.selectbox("Select Goal", gm.get_goals()['Goal Name'].values, key="selected_goal")
                allocation_amount = st.number_input("Allocation Amount (EUR)", min_value=0.0, key="allocation_amount")
                
                if st.button("Allocate", key="allocate_button"):
                    if allocation_amount > 0:
                        gm.allocate_to_goal(selected_goal, allocation_amount)
                        st.success(f"Allocated {allocation_amount} EUR to '{selected_goal}'")
                    else:
                        st.error("Please enter a valid allocation amount.")
            else:
                st.write("No goals available. Please create a goal first.")

    # Display updated goal progress
    st.write("### Updated Financial Goals")
    st.dataframe(gm.track_goal_progress())
