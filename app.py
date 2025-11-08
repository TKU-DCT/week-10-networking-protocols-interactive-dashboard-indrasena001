import streamlit as st
import sqlite3
import pandas as pd
import time
import os

DB_NAME = "log.db"

st.set_page_config(page_title="Networking & Protocols Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Select Page", ["Dashboard", "Settings", "About"])

# TODO: Check if database exists
if not os.path.exists(DB_NAME):
    st.warning("Database not found. Please make sure 'log.db' from Week 7–8 exists.")
else:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM system_log", conn)

    if page == "Dashboard":
        st.title("🌐 Interactive Data Center Dashboard")

        # TODO: Add auto-refresh or manual refresh
        # Hint: use st.button("Refresh") or st.experimental_rerun()

        # TODO: Add sidebar filters (Ping Status, CPU Threshold)
        # Example: selectbox + slider

        # TODO: Apply filters to dataframe
        st.subheader("Filtered Records")
        st.dataframe(df, use_container_width=True)

        # TODO: Add line charts for CPU, Memory, Disk
        st.subheader("📈 Resource Usage Over Time")
        st.line_chart(df.set_index("timestamp")[["cpu", "memory", "disk"]])

    elif page == "Settings":
        st.title("⚙️ Settings Page")
        st.write("You can add custom configuration or thresholds here.")
    else:
        st.title("ℹ️ About")
        st.write("This dashboard was developed in Week 10 (Networking & Protocols).")

    conn.close()
