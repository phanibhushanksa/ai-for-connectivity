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

# Function to clear chat history
def clear_chat():
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

# with col2:
#     st.subheader("Network Log Analysis")

#     # Log analysis controls
#     time_range = st.selectbox(
#         "Select Time Range",
#         ["Last Hour", "Last 24 Hours", "Last Week"],
#         key="time_range"
#     )

#     if st.button("Analyze Logs", key="analyze_button"):
#         with st.spinner("Analyzing network logs..."):
#             try:
#                 # Get network logs
#                 logs = get_network_logs(time_range)

#                 # Analyze logs
#                 analysis_results = analyze_logs(logs)

#                 # Prepare findings for Groq API
#                 findings_prompt = "Analyze these network log findings and provide specific resolutions:\n"
#                 findings_prompt += "\n".join([f"- {finding}" for finding in analysis_results["findings"]])
#                 findings_prompt += "\n\nFor each finding, provide a clear resolution or recommendation."

#                 # Get resolutions from Groq API
#                 with st.spinner("Getting AI-powered resolutions..."):
#                     groq_response = get_groq_response(findings_prompt)

#                 # Parse Groq response into individual resolutions
#                 # Assuming response comes as a list or numbered items
#                 resolutions = []
#                 for line in groq_response.split('\n'):
#                     if line.strip() and not line.strip().startswith(('Findings:', 'Recommendations:')):
#                         resolutions.append(line.strip())

#                 # Ensure we have matching number of resolutions
#                 while len(resolutions) < len(analysis_results["findings"]):
#                     resolutions.append("No specific resolution provided.")

#                 # Display results
#                 st.success("Analysis Complete")

#                 # Display findings and recommendations side by side
#                 st.subheader("Analysis Results")
#                 col_findings, col_recommendations = st.columns(2)

#                 with col_findings:
#                     st.markdown("**Findings**")
#                     for finding in analysis_results["findings"]:
#                         st.info(finding)

#                 with col_recommendations:
#                     st.markdown("**Recommendations**")
#                     for resolution in resolutions:
#                         st.warning(resolution)

#             except Exception as e:
#                 st.error(f"Error analyzing logs: {str(e)}")

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
                # Get network logs (predefined dummy logs)
                logs = get_network_logs(time_range)

                # Analyze logs (extracts dummy issues)
                analysis_results = analyze_logs(logs)

                # Prepare issues for Groq API
                issues_prompt = """
                Analyze these network log issues and provide specific resolutions:
                {issues}

                For each issue:
                1. Provide a clear, actionable recommendation
                2. Include any relevant commands or steps where applicable
                3. Keep responses technical and concise
                """
                issues_prompt = issues_prompt.format(
                    issues="\n".join([f"- {issue}" for issue in analysis_results["findings"]])
                )

                # Get recommendations from Groq API
                with st.spinner("Getting AI-powered recommendations..."):
                    groq_response = get_groq_response(issues_prompt)

                # Parse Groq response into individual recommendations
                recommendations = []
                for line in groq_response.split('\n'):
                    line = line.strip()
                    if line and not line.startswith(('Issues:', 'Recommendations:')):
                        if line.startswith(('- ', '* ', '1. ', '2. ', '3. ')):
                            line = line[2:].strip()
                        recommendations.append(line)

                # Ensure we have matching number of recommendations
                while len(recommendations) < len(analysis_results["findings"]):
                    recommendations.append("No specific recommendation provided.")

                # Display results
                st.success("Analysis Complete")

                # Display issues and recommendations side by side
                st.subheader("Analysis Results")
                col_issues, col_recommendations = st.columns(2)

                with col_issues:
                    st.markdown("**Issues**")
                    for i, issue in enumerate(analysis_results["findings"], 1):
                        if issue.startswith("Warning:"):
                            st.warning(f"{i}. {issue}")
                        elif issue.startswith("Error:"):
                            st.error(f"{i}. {issue}")

                with col_recommendations:
                    st.markdown("**Recommendations**")
                    for i, recommendation in enumerate(recommendations, 1):
                        st.info(f"{recommendation}")

            except Exception as e:
                st.error(f"Error analyzing logs: {str(e)}")
