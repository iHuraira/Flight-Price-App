import streamlit as st

st.title("📊 Indian Flight Price Dataset Overview")

st.markdown("""
### ✈️ Dataset Summary

The dataset contains **206,774** flight records from Indian airlines with details on schedules, cities, and ticket prices.

**🧾 Total Entries:** `206,774`  
**🧱 Columns:** `11`  
**📦 Memory Usage:** ~`17.4 MB`  
**✅ Missing Values:** None — all columns are complete

---
### 🧩 Column Breakdown

| Column       | Description                                                       | Type     |
|--------------|-------------------------------------------------------------------|----------|
| `date`       | Date of the scheduled flight                                      | Object   |
| `airline`    | Name of the airline operating the flight                          | Object   |
| `ch_code`    | Airline code (unique per airline)                                 | Object   |
| `num_code`   | Unique flight code                                                | Integer  |
| `dep_time`   | Scheduled departure time                                          | Object   |
| `from`       | Departure city                                                    | Object   |
| `time_taken` | Total flight duration (e.g., "02h 15m")                           | Object   |
| `stop`       | Indicates stop type (`non-stop`, `1-stop`, etc.)                 | Object   |
| `arr_time`   | Scheduled arrival time                                            | Object   |
| `to`         | Arrival city                                                      | Object   |
| `price`      | Ticket price (as text, needs cleaning for numeric usage)         | Object   |

---
### 🧠 Insights

- The dataset is clean with no nulls.
- Most fields are categorical/text, ideal for encoding.
- `price` is stored as text and may require conversion for modeling.
- Could be useful for building price predictors, time estimators, or airline analytics.
""")

footer = """
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #f1f1f1;
    color: #000;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #e1e1e1;
}
</style>
<div class="footer">
    ⏱️ Built with ❤️ using Streamlit | © 2025 Your Name or Company
</div>
"""

st.markdown(footer, unsafe_allow_html=True)