import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="SysPulse Dashboard", layout="wide")

st.title("🚀 SysPulse: System Monitoring")

CSV_PATH = "logs/metrics_history.csv"

def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return df
    return None

#Sidebar
st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (sec)", 1, 10, 5)

#Main dashboard loop
placeholder = st.empty()

while True:
    df = load_data()
    
    with placeholder.container():
        if df is not None:
            #Filter data for CPU and Memory usage
            cpu_df = df[df['metric'] == 'usage_percent'][['timestamp', 'value']]
            mem_df = df[df['metric'] == 'percent_used'][['timestamp', 'value']]

            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("CPU Usage (%)")
                st.line_chart(cpu_df.set_index('timestamp'))

            with col2:
                st.subheader("Memory Usage (%)")
                st.line_chart(mem_df.set_index('timestamp'))
                
            st.write("Last Data:")
            st.dataframe(df.tail(10))
        else:
            st.error("CSV file not found. Please start the monitoring!")

    time.sleep(refresh_rate)