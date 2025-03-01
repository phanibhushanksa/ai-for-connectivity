import streamlit as st
from utils.groq_client import get_groq_response

st.set_page_config(
    page_title="AI Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 AI Network Assistant")

# Create two columns for the split view

st.subheader("Network Troubleshooting Assistant")

# Add a check for API key
if not st.session_state.get("api_key_checked"):
    with st.spinner("Checking API configuration..."):
        try:
            # Test API connection
            test_response = get_groq_response("test")
            st.session_state.api_key_checked = True
        except Exception as e:
            st.error("Error: Unable to connect to Groq API. Please check your API key.")
            st.stop()

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about network issues..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.spinner("Thinking..."):
        try:
            response = get_groq_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")

