# Week 10 – Networking & Protocols: Interactive Dashboard

## Objective

This week, you will enhance your Streamlit dashboard with **interactive controls** and use **real data**
from your monitoring system (`log.db` generated in Week 7–8).

---

## Data Source

Your dashboard uses the **same database** you created in:
- Week 7 (SQLite Logging)
- Week 8 (Alert System Updates)

If your `log.db` file is missing or empty, please re-run your Week 8 `main.py`
to generate log entries before running this assignment.

---

## Tasks

1. Add a **sidebar navigation menu**:
   - Dashboard
   - Settings
   - About
2. Implement **auto-refresh** or **manual refresh** button.
3. Add **filter controls**:
   - Ping_Status (All / UP / DOWN)
   - CPU Threshold slider
4. Display filtered data and charts for CPU, Memory, Disk.
5. Include a short description on the Settings and About pages.

---

## Example Output

- Sidebar with navigation
- Filtered data table
- Dynamic line charts
- Refresh button or timer

---

## Run the Dashboard

```bash
streamlit run app.py
```

Make sure log.db is in the same directory.

## Submission Checklist

 app.py includes sidebar, filters, and refresh

 Charts render correctly

 Screenshot of dashboard with filters

 Code pushed to GitHub
 ---

## Bonus (Optional)

Add a date filter using st.date_input

Display alert count (how many records exceeded thresholds)

Add Dark Mode toggle in the Settings page
