import plotly.express as px
import streamlit as st

import pandas as pd

# Configure the page
st.set_page_config(page_title="Network Monitoring Dashboard",
                   page_icon="🌐",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.title("📊 Network Monitoring Dashboard")

df_network_traffic = pd.read_csv('data/network_traffic.csv')

network_traffic_cols = df_network_traffic.columns[:4]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label=network_traffic_cols[0],
              value=int(df_network_traffic[network_traffic_cols[0]].sum()))

with col2:
    st.metric(label=network_traffic_cols[1],
              value=int(df_network_traffic[network_traffic_cols[1]].sum()))

with col3:
    st.metric(label=network_traffic_cols[2],
              value=int(df_network_traffic[network_traffic_cols[2]].sum()))

with col4:
    st.metric(label=network_traffic_cols[3],
              value=int(df_network_traffic[network_traffic_cols[3]].sum()))

col1, col2 = st.columns(2)
with col1:
    ## Memory Utilization Over Time
    st.subheader("Memory Utilization Over Time")
    df_memory = pd.read_csv('data/memory_utilization.csv')
    fig = px.line(df_memory,
                  x='time',
                  y='memory_utilization',
                  labels={
                      'memory_utilization': 'Memory Utilization (%)',
                      'time': 'Time'
                  })
    fig.update_yaxes(range=[0, 100])

    st.plotly_chart(fig)

with col2:
    ## CPU Utilization Over Time
    st.subheader("CPU Utilization Over Time")
    df_cpu = pd.read_csv('data/cpu_utilization.csv')
    fig = px.line(df_cpu,
                  x='time',
                  y='cpu_utilization',
                  labels={
                      'cpu_utilization': 'CPU Utilization (%)',
                      'time': 'Time'
                  })
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig)

## System Load
st.subheader("System Load")
df_system_load = pd.read_csv('data/system_load.csv')
fig = px.line(df_system_load,
              x='Timestamp',
              y=['Load Avg (1m)', 'Load Avg (5m)', 'Load Avg (15m)'],
              template='plotly_dark',
              height=400)
st.plotly_chart(fig)

with col1:
    ## Network Traffic Over Time
    st.subheader("Network Traffic Over Time")
    df_network_traffic[
        'Bits Received'] = df_network_traffic['Bits Received'] / 1024
    df_network_traffic['Bits Sent'] = df_network_traffic['Bits Sent'] / 1024

    fig = px.area(df_network_traffic,
                  x='Timestamp',
                  y=['Bits Received', 'Bits Sent'],
                  labels={
                      'value': 'Bytes (MB)',
                      'Timestamp': 'Time'
                  })
    st.plotly_chart(fig)
with col2:
    # Create stacked bar chart
    st.subheader("Packet Types Discarded Over Time")
    fig = px.bar(df_network_traffic,
                 x='Timestamp',
                 y=[
                     'Inbound packets discarded', 'Outbound packets discarded',
                     'Inbound packets with errors',
                     'Outbound packets with errors'
                 ],
                 labels={
                     'value': 'Packets Count',
                     'Timestamp': 'Time'
                 },
                 template='plotly_dark',
                 height=400)

    # Show the chart in Streamlit
    st.plotly_chart(fig)

## Operational Status
# st.subheader("Operational Status")
# df_status = pd.read_csv('data/operational_status.csv')
# st.dataframe(df_status)
