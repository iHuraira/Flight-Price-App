import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

dashboard_page = st.Page(
    page="./src/components/pages/Dashboard.py",
    title="Dashboard",
    icon=":material/bar_chart_4_bars:",
)

about_page = st.Page(
    page="./src/components/pages/about_me.py",
    title="About me",
    icon=":material/account_circle:",
)

about_data = st.Page(
    page="./src/components/pages/about_data.py",
    title="About data",
    icon=":material/description:",
)

predictor_page = st.Page(
    page="./src/components/pages/predictor.py",
    title="Predictor",
    icon=":material/online_prediction:",
    default=True
)

pg = st.navigation({
    "App" : [dashboard_page, predictor_page,  about_data],
    "Info" : [about_page]
})

# This is the new project

pg.run()