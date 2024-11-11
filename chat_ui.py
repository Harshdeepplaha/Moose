import streamlit as st
from llm_chat import generate_chat_response

def render_chat_ui(df):
    """
    Renders the chat interface for interacting with the financial assistant LLM.
    
    Parameters:
    - df (DataFrame): The user's categorized transaction data.
    """
    st.sidebar.title("Chat with Financial Assistant")

    # Initialize session state for chat history if it doesn’t exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history in a scrollable container
    with st.sidebar.container():
        st.write("Chat History:")
        chat_messages = st.sidebar.empty()  # Placeholder for chat messages

        # Display all messages in session history in a scrollable area
        chat_history_html = ""
        for question, response in st.session_state.chat_history:
            chat_history_html += f"<p><b>You:</b> {question}</p><p><b>Assistant:</b> {response}</p><hr>"

        # Render the chat history HTML with scrollable styling
        chat_messages.markdown(
            f"<div style='max-height: 300px; overflow-y: auto; padding: 10px;'>{chat_history_html}</div>",
            unsafe_allow_html=True
        )

    # Input for user's question at the bottom of the chat sidebar
    user_question = st.sidebar.text_input("Ask a question about your finances:", key="user_question_input")

    # Trigger response on question submission
    if st.sidebar.button("Ask"):
        if user_question.strip():
            # Generate response and add it to chat history
            response = generate_chat_response(user_question, df)
            st.session_state.chat_history.append((user_question, response))

            # Use a placeholder to clear the input after submission
            st.sidebar.text_input("Ask a question about your finances:", key="user_question_input_clear", value="")

    # Clear chat history button
    if st.sidebar.button("Clear Chat History"):
        st.session_state.chat_history = []
