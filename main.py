import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Network Monitor",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
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
    .featured-section {
        
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
            unsafe_allow_html=True)

st.markdown('<p class="home"></p>', unsafe_allow_html=True)
st.image(image="images/Network-Repair.jpg", use_container_width=True)

st.title("🌐 AI Powered Network Monitoring System")
st.markdown("""
Welcome to the AI Powered Network Monitoring System home page.
Use the sidebar to explore:
- 📊 **DASHBOARD**: Keep track of network status with real-time metrics and monitoring.
- 🤖 **AI ASSISTANT**: Leverage AI for troubleshooting and detailed network analysis.
- 👥 **ABOUT US**: Meet the team behind this project.
""")

# Zabbix Information Section
st.markdown("""
<div class="featured-section">
<h2>🔍 Powered by Zabbix</h2>
<p>Our system integrates with <b>Zabbix</b>, an enterprise-class open-source monitoring solution designed for real-time monitoring of servers, networks, and applications. Zabbix provides:</p>
<ul>
<li>Advanced monitoring capabilities with distributed monitoring</li>
<li>Real-time notifications and alerting</li>
<li>Extensive data collection options including SNMP, IPMI, and JMX monitoring</li>
<li>Customizable dashboards and visualization tools</li>
<li>Auto-discovery of network devices and configuration</li>
</ul>
</div>
""",
            unsafe_allow_html=True)

# GigaAI Hackathon Section
st.markdown("""
<div class="featured-section">
<h2>🏆 GigaAI Hackathon Project</h2>
<p>This solution was developed as part of the <b>GigaAI Hackathon</b>, where teams competed to create innovative AI-powered solutions for real-world problems.</p>
<p>Our project focuses on revolutionizing network monitoring by combining traditional monitoring tools with cutting-edge AI techniques to create a more intelligent, proactive monitoring system that:</p>
<ul>
<li>Predicts potential network issues before they occur</li>
<li>Reduces mean time to resolution (MTTR) for network problems</li>
<li>Provides actionable insights without requiring deep networking expertise</li>
<li>Streamlines troubleshooting workflows for IT teams</li>
</ul>
</div>
""",
            unsafe_allow_html=True)

# AI Assistant Benefits Section
st.markdown("""
<div class="featured-section">
<h2>🚀 How Our AI Assistant Helps Network Engineers</h2>
<p>Our AI-powered assistant is specifically designed to help network engineers troubleshoot issues more efficiently:</p>
<ul>
<li><b>Intelligent Log Analysis:</b> Automatically parses through network logs to identify patterns and anomalies</li>
<li><b>Root Cause Analysis:</b> Identifies the underlying causes of network issues, not just the symptoms</li>
<li><b>Step-by-Step Resolution:</b> Provides clear, actionable guidance to resolve network problems</li>
<li><b>Network Best Practices:</b> Offers recommendations based on industry best practices</li>
<li><b>Knowledge Base:</b> Continually learns from new issues to improve future recommendations</li>
<li><b>Reduced Downtime:</b> Helps engineers resolve issues faster, minimizing network downtime</li>
</ul>
<p>Whether you're dealing with latency issues, connection problems, or bandwidth constraints, our AI assistant can guide you through the troubleshooting process with expert-level recommendations.</p>
</div>
""",
            unsafe_allow_html=True)

# Call to action
st.markdown("---")
st.markdown("### Ready to explore?")
st.markdown(
    "Navigate to the **Dashboard** to view your network metrics or try the **AI Assistant** to troubleshoot network issues."
)
