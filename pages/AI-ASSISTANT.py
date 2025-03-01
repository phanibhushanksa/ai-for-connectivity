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

# Function to clear chat history
def clear_chat():
    st.session_state.messages = []

st.title("🤖 AI Network Assistant")

st.subheader("Network Troubleshooting Assistant")

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

# Add session state for clear chat
if "clear_chat_clicked" not in st.session_state:
    st.session_state.clear_chat_clicked = False
    
def handle_clear_chat():
    clear_chat()
    st.session_state.clear_chat_clicked = True
    
# Add clear chat button
if st.button("Clear Chat History", type="secondary", on_click=handle_clear_chat):
    pass
    
# Check if we need to rerun after clearing chat
if st.session_state.clear_chat_clicked:
    st.session_state.clear_chat_clicked = False
    st.rerun()

# Suggested questions
st.subheader("Suggested Questions")
question_col1, question_col2, question_col3 = st.columns(3)

suggested_questions = [
    "How do I troubleshoot high network latency?",
    "What causes DNS resolution failures?",
    "How to optimize network bandwidth usage?"
]

# Use session state to trigger API call when a suggested question is clicked
if "suggested_question" not in st.session_state:
    st.session_state.suggested_question = None

def set_question(question):
    st.session_state.suggested_question = question

question_col1.button(suggested_questions[0], on_click=set_question, args=(suggested_questions[0],))
question_col2.button(suggested_questions[1], on_click=set_question, args=(suggested_questions[1],))
question_col3.button(suggested_questions[2], on_click=set_question, args=(suggested_questions[2],))

# Process the suggested question if one was clicked
if st.session_state.suggested_question:
    question = st.session_state.suggested_question
    st.session_state.suggested_question = None
    
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Get AI response
    with st.spinner("Thinking..."):
        try:
            response = get_groq_response(question)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.rerun()

st.markdown("---")

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
