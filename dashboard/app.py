import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Network Intrusion Detection Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Network Intrusion Detection & Real-Time Monitoring System")
st.markdown("Monitor network flows, test simulated traffic, and review security alerts in real-time.")

# Sidebar for testing traffic
st.sidebar.header("🧪 Test Network Traffic")
duration = st.sidebar.number_input("Duration (s)", value=1.5, min_value=0.0)
protocol = st.sidebar.selectbox("Protocol", [6, 17, 1], format_func=lambda x: "TCP (6)" if x==6 else ("UDP (17)" if x==17 else "ICMP (1)"))
src_port = st.sidebar.number_input("Source Port", value=12345, min_value=1, max_value=65535)
dst_port = st.sidebar.selectbox("Destination Port", [80, 443, 22, 8080, 3389])
packet_size = st.sidebar.slider("Packet Size (bytes)", min_value=50, max_value=1500, value=500)
flow_Bytes_s = st.sidebar.number_input("Flow Bytes/s", value=1500.0, min_value=0.0)

if st.sidebar.button("Analyze Traffic"):
    payload = {
        "duration": duration,
        "protocol": protocol,
        "src_port": src_port,
        "dst_port": dst_port,
        "packet_size": packet_size,
        "flow_Bytes_s": flow_Bytes_s
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            res = response.json()
            if res["prediction"] == "Attack":
                st.sidebar.error(f"🚨 ALERT! Prediction: {res['prediction']} (Confidence: {res['confidence']:.2f})")
            else:
                st.sidebar.success(f"✅ Safe! Prediction: {res['prediction']} (Confidence: {res['confidence']:.2f})")
        else:
            st.sidebar.error("Error communicating with backend API.")
    except Exception as e:
        st.sidebar.error(f"Could not connect to FastAPI backend. Is it running? Error: {e}")

# Main body: Display Alert History from Backend
st.subheader("📊 Recent Security Alerts Log")

if st.button("Refresh Alerts"):
    st.rerun()

try:
    api_response = requests.get("http://127.0.0.1:8000/alerts")
    if api_response.status_code == 200:
        data = api_response.json()
        total_alerts = data["total_alerts"]
        alerts_list = data["alerts"]
        
        st.metric(label="Total Recorded Attack Alerts", value=total_alerts)
        
        if total_alerts > 0:
            df_alerts = pd.DataFrame(alerts_list, columns=["ID", "Timestamp", "Source Port", "Destination Port", "Packet Size", "Confidence", "Status"])
            st.dataframe(df_alerts, use_container_width=True)
        else:
            st.info("No security alerts logged yet. Try simulating suspicious traffic (e.g., packet size > 850) from the sidebar!")
    else:
        st.warning("Could not fetch alerts from backend.")
except Exception:
    st.warning("⚠️ FastAPI backend is currently offline. Start the backend server to view live database alerts.")