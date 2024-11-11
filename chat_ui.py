# chat_ui.py
import streamlit as st
from langchain_community.llms import Ollama

# Initialize the local Ollama LLM
llm = Ollama(model="llama2")  # Specify your model name if different

def chat_ui(df):
    st.sidebar.header("Chatbot")
    st.sidebar.write("Ask questions about your transactions, spending patterns, or financial goals.")

    # User input for question
    user_question = st.sidebar.text_input("Type your question here:")
    if user_question:
        # Prepare the data context and prompt for the LLM
        data_context = df.to_dict(orient="records")  # Convert data to dictionary format
        prompt = f"{user_question} based on my transaction data: {data_context}"
        
        # Query the LLM
        llm_response = llm.invoke(prompt)
        
        # Display response
        st.sidebar.write("LLM Response:", llm_response)
