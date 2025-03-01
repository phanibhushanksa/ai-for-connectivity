import streamlit as st
from utils.groq_client import get_groq_response
from utils.network_logs import get_network_logs, analyze_logs

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
col1, col2 = st.columns(2)

with col1:
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

with col2:
    st.subheader("Network Log Analysis")

    # Log analysis controls
    time_range = st.selectbox(
        "Select Time Range",
        ["Last Hour", "Last 24 Hours", "Last Week"],
        key="time_range"
    )

    if st.button("Analyze Logs", key="analyze_button"):
        with st.spinner("Analyzing network logs..."):
            try:
                # Get network logs
                logs = get_network_logs(time_range)

                # Analyze logs
                analysis_results = analyze_logs(logs)

                # Display results
                st.success("Analysis Complete")

                # Display findings
                st.subheader("Findings")
                for finding in analysis_results["findings"]:
                    st.info(finding)

                # Display recommendations
                st.subheader("Recommendations")
                for rec in analysis_results["recommendations"]:
                    st.warning(rec)

            except Exception as e:
                st.error(f"Error analyzing logs: {str(e)}")