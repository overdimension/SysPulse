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


#Main dashboard loop
placeholder = st.empty()

while True:
    df = load_data()
    
    with placeholder.container():
        if df is not None:
            #Getting the latest values ​​for the cards
            try:
                last_cpu = df[df['metric'] == 'usage_percent']['value'].iloc[-1]
                mem_data = df[df['collector'] == 'memory']
                last_mem = mem_data['value'].iloc[-1] if not mem_data.empty else 0
                disk_data = df[df['collector'] == 'disk']
                last_disk = disk_data['value'].iloc[-1] if not disk_data.empty else 0
            except(IndexError, KeyError):
                last_cpu, last_mem, last_disk = 0, 0, 0

            #Main indicators
            m1, m2, m3 = st.columns(3)
            m1.metric("CPU Load", f"{last_cpu}%")
            m2.metric("Memory Usage", f"{last_mem}%")
            m3.metric("Disk Usage", f"{last_disk}%")

            st.divider()

            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 CPU History")
                cpu_history = df[df['metric'] == 'usage_percent'].tail(50)
                st.line_chart(cpu_history.set_index('timestamp')['value'])

            with col2:
                st.subheader("📈 Memory History")
                mem_history = df[(df['collector'] == 'memory') & (df['metric'] == 'percent_used')].tail(50)
                st.line_chart(mem_history.set_index('timestamp')['value'])

            st.subheader("📝 Last Records in Database")
            st.dataframe(df.tail(15), width="stretch")
        else:
            st.warning("⏳ Waiting for data... Make sure the collectors are running and writing to the CSV file.")

    time.sleep(2)