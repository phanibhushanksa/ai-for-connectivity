from datetime import datetime, timedelta

def get_network_logs(time_range: str) -> list:
    """
    Simulate fetching network logs with predefined dummy issues
    """
    # Define dummy issues for each time range with timestamps
    dummy_logs = {
        "Last Hour": [
            {"timestamp": datetime.now() - timedelta(minutes=45), "type": "Warning: High latency detected on interface eth0", "severity": "MEDIUM", "details": "Event detected on interface eth0"},
            {"timestamp": datetime.now() - timedelta(minutes=30), "type": "Error: DNS resolution failed for domain example.com", "severity": "HIGH", "details": "Event detected on interface eth1"}
        ],
        "Last 24 Hours": [
            {"timestamp": datetime.now() - timedelta(hours=20), "type": "Warning: Packet loss detected on subnet 10.0.0.0/24", "severity": "MEDIUM", "details": "Event detected on interface eth0"},
            {"timestamp": datetime.now() - timedelta(hours=15), "type": "Error: Firewall dropped connection from 203.0.113.1", "severity": "HIGH", "details": "Event detected on interface eth2"},
            {"timestamp": datetime.now() - timedelta(hours=10), "type": "Warning: Bandwidth usage exceeded 90% on port 443", "severity": "MEDIUM", "details": "Event detected on interface eth1"},
            {"timestamp": datetime.now() - timedelta(hours=5), "type": "Error: TCP retransmission rate exceeded threshold on server1", "severity": "HIGH", "details": "Event detected on interface eth3"},
            {"timestamp": datetime.now() - timedelta(hours=2), "type": "Warning: Intermittent connectivity on VLAN 10", "severity": "MEDIUM", "details": "Event detected on interface eth0"}
        ],
        "Last Week": [
            {"timestamp": datetime.now() - timedelta(days=6, hours=12), "type": "Warning: Unusual traffic pattern on port 8080", "severity": "MEDIUM", "details": "Event detected on interface eth2"},
            {"timestamp": datetime.now() - timedelta(days=5, hours=8), "type": "Error: Switch port 5 down", "severity": "HIGH", "details": "Event detected on interface eth1"},
            {"timestamp": datetime.now() - timedelta(days=4, hours=16), "type": "Warning: High CPU usage on router R1", "severity": "MEDIUM", "details": "Event detected on interface eth0"},
            {"timestamp": datetime.now() - timedelta(days=4), "type": "Error: Authentication failure for VPN connection", "severity": "HIGH", "details": "Event detected on interface eth3"},
            {"timestamp": datetime.now() - timedelta(days=3, hours=12), "type": "Warning: Low disk space on network monitor", "severity": "MEDIUM", "details": "Event detected on interface eth2"},
            {"timestamp": datetime.now() - timedelta(days=3), "type": "Error: OSPF neighbor adjacency lost with 192.168.1.2", "severity": "HIGH", "details": "Event detected on interface eth1"},
            {"timestamp": datetime.now() - timedelta(days=2, hours=8), "type": "Warning: High jitter detected in VoIP traffic", "severity": "MEDIUM", "details": "Event detected on interface eth0"},
            {"timestamp": datetime.now() - timedelta(days=2), "type": "Error: SSL certificate expired on load balancer", "severity": "HIGH", "details": "Event detected on interface eth3"},
            {"timestamp": datetime.now() - timedelta(days=1, hours=12), "type": "Warning: Multiple failed login attempts on switch S1", "severity": "MEDIUM", "details": "Event detected on interface eth2"},
            {"timestamp": datetime.now() - timedelta(hours=12), "type": "Error: Storage array network path failure", "severity": "HIGH", "details": "Event detected on interface eth1"}
        ]
    }

    # Return the predefined logs for the selected time range
    return dummy_logs.get(time_range, [])

def analyze_logs(logs: list) -> dict:
    """
    Analyze network logs and provide insights aligned with dummy issues
    """
    # Extract issues from logs
    issues = [log["type"] for log in logs]  # Use the type field directly as issues

    # For compatibility with the original structure, we'll count severity but not use it for findings
    severity_count = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for log in logs:
        severity_count[log["severity"]] += 1

    # Generate findings (just return the issues as-is since they're predefined)
    findings = issues

    # We'll let Groq API generate recommendations, so return empty recommendations here
    recommendations = []

    return {
        "findings": findings,  # Now contains "Warning:" and "Error:" prefixed issues
        "recommendations": recommendations
    }