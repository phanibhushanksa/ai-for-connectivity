import streamlit as st
from utils.network_logs import get_network_logs, analyze_logs


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