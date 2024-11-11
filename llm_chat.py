# # llm_chat.py

# import pandas as pd
# from model import initialize_llm  # Import model initialization
# import metrics  # Import metrics functions
# import streamlit as st
# from goal_manager import get_goals, get_goal_details  # Import goal retrieval functions

# # Initialize LLM instance
# llm = initialize_llm()

# def generate_goal_prompt(goal):
#     """Generate a suggestion prompt for a specific goal."""
#     name = goal['Goal Name']
#     target = goal['Target Amount']
#     current_saved = goal['Current Amount Saved']
#     target_date = goal['Target Date']
    
#     return (
#         f"I have a financial goal named '{name}' with a target of €{target}."
#         f"Currently, I have saved €{current_saved}. The deadline to achieve this goal is {target_date}. "
#         "Please provide suggestions on how I can reach this goal faster and any steps I can take to improve my finances."
#     )

# def generate_chat_response(user_question, df):
#     keyword_to_command = {
#         "total expenses": "total expenses",
#         "total income": "total income",
#         "net savings": "net savings",
#         "top spending categories": "top spending categories",
#         "top income categories": "top income categories",
#         "monthly growth rate": "monthly growth rate",
#         "yearly summary": "yearly summary",
#         "budget variance": "budget variance",
#         "savings rate": "savings rate",
#         "income to expense ratio": "income to expense ratio",
#         "spending consistency": "spending consistency",
#         "recurring expenses": "recurring expenses",
#         "average transaction size": "average transaction size",
#         "highest transaction": "highest transaction",
#         "lowest transaction": "lowest transaction",
#         "monthly breakdown": "monthly breakdown",
#         "yearly breakdown": "yearly breakdown",
#         "expense by category": "expense by category",
#         "income by category": "income by category",
#         "savings goal progress": "savings goal progress",
#     }

#     # Check if user is asking for goal-related suggestions
#     if "suggestion" in user_question.lower() and "goal" in user_question.lower():
#         goals = get_goals()
        
#         # Check if there are any goals
#         if goals.empty:
#             st.write("No goals found. Please create a goal first.")
#             return

#         # Generate suggestions for each goal
#         suggestions = []
#         for _, goal in goals.iterrows():
#             prompt = generate_goal_prompt(goal)
#             response = llm.invoke(prompt)  # Replace with the LLM call
#             suggestions.append(f"**{goal['Goal Name']}**: {response}")
        
#         # Display all goal suggestions
#         st.write("\n\n".join(suggestions))
#         return

#     # Process keyword-to-command mapping for regular financial metrics
#     for keyword, command in keyword_to_command.items():
#         if keyword in user_question.lower():
#             result, plot_func = metrics.execute_command(command, df)

#             # Display metric result
#             if isinstance(result, pd.Series):  # Monthly or yearly breakdown
#                 result_str = "\n".join([f"{index}: €{value:,.2f}" for index, value in result.items()])
#                 st.write(f"Here is the breakdown of your {command}:\n{result_str}")
#             elif isinstance(result, tuple):  # Max or min spending (returns a transaction and amount)
#                 st.write(f"The {command} is '{result[0]}' with an amount of €{result[1]:,.2f}.")
#             else:
#                 st.write(f"The {command} is €{result:,.2f}.")

#             # Display associated plot if available
#             if plot_func:
#                 fig = plot_func(result, title=command.title().replace("_", " "))
#                 st.plotly_chart(fig)  # Use st.plotly_chart for Plotly figures

#             return

#     # Fallback to LLM if no metric match
#     st.write("No specific metric found. Generating response from the LLM...")
#     data_summary = df[['Date', 'Name / Description', 'Expense/Income', 'Amount (EUR)', 'Category']].head(5).to_string(index=False)
#     prompt = (
#         f"You are an AI financial assistant. The user has the following question: '{user_question}'. "
#         f"Here is a sample of the user's transaction data:\n\n{data_summary}\n\n"
#         "Answer the question based on this data, providing insights if possible."
#     )
    
#     # Generate response from LLM
#     try:
#         response = llm.invoke(prompt)
#         st.write(response)
#     except Exception as e:
#         print(f"Error generating chat response: {e}")
#         st.write("I'm sorry, I encountered an error while processing your request.")

# llm_chat.py

import pandas as pd
import whisper
import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from model import initialize_llm
import metrics
from goal_manager import get_goals, get_goal_details

# Initialize LLM instance and Whisper model
llm = initialize_llm()
whisper_model = whisper.load_model("base")

class WhisperAudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.transcribed_text = ""

    def recv(self, frame):
        audio_data = frame.to_ndarray()
        result = whisper_model.transcribe(audio_data)
        self.transcribed_text = result["text"]

    def get_transcription(self):
        return self.transcribed_text

def generate_goal_prompt(goal):
    name = goal['Goal Name']
    target = goal['Target Amount']
    current_saved = goal['Current Amount Saved']
    target_date = goal['Target Date']
    
    return (
        f"I have a financial goal named '{name}' with a target of €{target}. "
        f"Currently, I have saved €{current_saved}. The deadline to achieve this goal is {target_date}. "
        "Please provide suggestions on how I can reach this goal faster and any steps I can take to improve my finances."
    )

def generate_chat_response(user_question, df):
    keyword_to_command = {
        "total expenses": "total expenses",
        "total income": "total income",
        "net savings": "net savings",
        "top spending categories": "top spending categories",
        "top income categories": "top income categories",
        # Other commands
    }

    if "suggestion" in user_question.lower() and "goal" in user_question.lower():
        goals = get_goals()
        if goals.empty:
            st.write("No goals found. Please create a goal first.")
            return

        suggestions = []
        for _, goal in goals.iterrows():
            prompt = generate_goal_prompt(goal)
            response = llm.invoke(prompt)
            suggestions.append(f"**{goal['Goal Name']}**: {response}")
        
        st.write("\n\n".join(suggestions))
        return

    for keyword, command in keyword_to_command.items():
        if keyword in user_question.lower():
            result, plot_func = metrics.execute_command(command, df)
            if isinstance(result, pd.Series):
                result_str = "\n".join([f"{index}: €{value:,.2f}" for index, value in result.items()])
                st.write(f"Here is the breakdown of your {command}:\n{result_str}")
            elif isinstance(result, tuple):
                st.write(f"The {command} is '{result[0]}' with an amount of €{result[1]:,.2f}.")
            else:
                st.write(f"The {command} is €{result:,.2f}.")
            if plot_func:
                fig = plot_func(result, title=command.title().replace("_", " "))
                st.plotly_chart(fig)
            return

    st.write("No specific metric found. Generating response from the LLM...")
    data_summary = df[['Date', 'Name / Description', 'Expense/Income', 'Amount (EUR)', 'Category']].head(5).to_string(index=False)
    prompt = (
        f"You are an AI financial assistant. The user has the following question: '{user_question}'. "
        f"Here is a sample of the user's transaction data:\n\n{data_summary}\n\n"
        "Answer the question based on this data, providing insights if possible."
    )
    
    try:
        response = llm.invoke(prompt)
        st.write(response)
    except Exception as e:
        print(f"Error generating chat response: {e}")
        st.write("I'm sorry, I encountered an error while processing your request.")

def main(df):
    processor = WhisperAudioProcessor()

    # Chat text input
    user_question = st.text_input("Ask a question about your finances:")

    # Add microphone button for voice input
    st.write("Or, use the microphone button below to ask a question by voice:")
    mic_button = st.button("🎙️ Start Voice Input")

    # If the microphone button is pressed, start capturing audio and transcribing
    if mic_button:
        webrtc_ctx = webrtc_streamer(
            key="voice_input",
            audio_processor_factory=lambda: processor,
            async_processing=True
        )

        # Display live transcription if available
        if processor.transcribed_text:
            user_question = processor.get_transcription()
            st.text_input("Transcribing...", value=user_question, disabled=True)

    # Process the question if it exists
    if user_question:
        generate_chat_response(user_question, df)
