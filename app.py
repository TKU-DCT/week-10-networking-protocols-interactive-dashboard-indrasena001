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
    # Ensure timestamp is parsed
    if "timestamp" in df.columns:
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        except Exception:
            pass

    if page == "Dashboard":
        st.title("🌐 Interactive Data Center Dashboard")

        # Refresh controls
        if st.sidebar.button("Refresh"):
            # Widget interactions already trigger a rerun in Streamlit.
            # Call experimental_rerun only if available to maintain compatibility across Streamlit versions.
            # Use getattr to avoid attribute access raising AttributeError on some Streamlit versions
            rerun = getattr(st, "experimental_rerun", None)
            if callable(rerun):
                rerun()

        # Filters in the sidebar
        st.sidebar.markdown("### Filters")
        ping_filter = st.sidebar.selectbox("Ping Status", ["All", "UP", "DOWN"], index=0)
        cpu_threshold = st.sidebar.slider("CPU Threshold (%)", 0, 100, 0)
        # Optional: date filter (bonus)
        try:
            min_date = df["timestamp"].min().date()
            max_date = df["timestamp"].max().date()
            date_range = st.sidebar.date_input("Date range", value=(min_date, max_date))
        except Exception:
            date_range = None

        # Apply filters
        df_filtered = df.copy()
        if ping_filter != "All" and "ping_status" in df_filtered.columns:
            df_filtered = df_filtered[df_filtered["ping_status"] == ping_filter]
        if "cpu" in df_filtered.columns:
            # keep records with cpu >= cpu_threshold so threshold acts as a minimum filter
            df_filtered = df_filtered[df_filtered["cpu"] >= cpu_threshold]
        if date_range and isinstance(date_range, tuple) and "timestamp" in df_filtered.columns:
            start_dt = pd.to_datetime(date_range[0])
            end_dt = pd.to_datetime(date_range[1])
            # include the whole end day
            end_dt = end_dt + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            df_filtered = df_filtered[(df_filtered["timestamp"] >= start_dt) & (df_filtered["timestamp"] <= end_dt)]

        st.subheader("Filtered Records")
        if df_filtered.empty:
            st.info("No records match the selected filters.")
        else:
            st.dataframe(df_filtered, width="stretch")

        # Alert count: records where cpu exceeds threshold OR ping is DOWN
        alert_count = 0
        if not df.empty:
            cond_cpu = df.get("cpu") > cpu_threshold if "cpu" in df.columns else pd.Series(False, index=df.index)
            cond_ping = df.get("ping_status") == "DOWN" if "ping_status" in df.columns else pd.Series(False, index=df.index)
            alert_count = int((cond_cpu | cond_ping).sum())

        col1, col2 = st.columns(2)
        col1.metric("Total records", len(df))
        col2.metric("Alert count", alert_count)

        # Charts
        st.subheader("📈 Resource Usage Over Time")
        if "timestamp" in df_filtered.columns and not df_filtered.empty:
            chart_df = df_filtered.set_index("timestamp")[ [c for c in ["cpu", "memory", "disk"] if c in df_filtered.columns] ]
            if not chart_df.empty:
                st.line_chart(chart_df)
        else:
            st.info("No time-series data available for the selected filters.")

    elif page == "Settings":
        st.title("⚙️ Settings Page")
        st.write("You can add custom configuration or thresholds here.")
    else:
        st.title("ℹ️ About")
        st.write("This dashboard was developed in Week 10 (Networking & Protocols).")

    conn.close()
