import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Network Monitoring Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Network Monitoring System")
st.markdown("""
Welcome to the Network Monitoring System dashboard. Use the sidebar to navigate between:
- 📊 **DASHBOARD**: Real-time network monitoring and metrics
- 🤖 **AI ASSISTANT**: AI-powered troubleshooting and network analysis
""")

# Default content for the main page
st.markdown("---")
st.markdown("### Quick Status Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Network Uptime", value="99.99%", delta="0.01%")
with col2:
    st.metric(label="Active Connections", value="1,234", delta="-12")
with col3:
    st.metric(label="Bandwidth Usage", value="42 Mbps", delta="5 Mbps")