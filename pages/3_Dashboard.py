import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.mock_data import generate_mock_metrics
import numpy as np

st.set_page_config(page_title="Network Dashboard", layout="wide")

# Generate mock data
metrics = generate_mock_metrics()

st.title("📊 Network Monitoring Dashboard")

# System Status Overview
st.subheader("System Status")
col1, col2, col3, col4 = st.columns(4)

status_indicators = {
    "Network": "🟢 Healthy",
    "Server Load": "🟡 Moderate",
    "Security": "🟢 Secure",
    "Storage": "🟢 OK"
}

for col, (metric, status) in zip([col1, col2, col3, col4], status_indicators.items()):
    col.metric(metric, status)

# Network Traffic Graph
st.subheader("Network Traffic")
fig_traffic = px.line(
    metrics["traffic_data"],
    x="timestamp",
    y="traffic",
    title="Network Traffic Over Time"
)
st.plotly_chart(fig_traffic, use_container_width=True)

# Server Resources
col1, col2 = st.columns(2)

with col1:
    # CPU Usage Gauge
    fig_cpu = go.Figure(go.Indicator(
        mode="gauge+number",
        value=metrics["cpu_usage"],
        title={"text": "CPU Usage"},
        gauge={"axis": {"range": [0, 100]},
               "bar": {"color": "darkblue"},
               "steps": [
                   {"range": [0, 50], "color": "lightgray"},
                   {"range": [50, 80], "color": "gray"}
               ],
               "threshold": {
                   "line": {"color": "red", "width": 4},
                   "thickness": 0.75,
                   "value": 90
               }}))
    st.plotly_chart(fig_cpu)

with col2:
    # Memory Usage Gauge
    fig_memory = go.Figure(go.Indicator(
        mode="gauge+number",
        value=metrics["memory_usage"],
        title={"text": "Memory Usage"},
        gauge={"axis": {"range": [0, 100]},
               "bar": {"color": "darkblue"},
               "steps": [
                   {"range": [0, 50], "color": "lightgray"},
                   {"range": [50, 80], "color": "gray"}
               ],
               "threshold": {
                   "line": {"color": "red", "width": 4},
                   "thickness": 0.75,
                   "value": 90
               }}))
    st.plotly_chart(fig_memory)

# Alert Log
st.subheader("Recent Alerts")
alert_df = pd.DataFrame(metrics["alerts"])
st.dataframe(alert_df, use_container_width=True)
