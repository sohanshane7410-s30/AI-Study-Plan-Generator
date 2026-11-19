import html
from typing import Any

import pandas as pd
import streamlit as st

from supabase_storage import (
    render_login_gate,
    load_student_records,
    load_study_plans,
    save_student_record,
    save_study_plan,
)


# =========================================================
# 1. APPLICATION CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Learning Intelligence Studio",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. PREMIUM DESIGN SYSTEM
# =========================================================

st.markdown(
    """
<style>
.stApp { background: #F5F6FC; color: #18213B; }
.block-container { max-width: 1500px; padding: 2rem 2.2rem 3rem; }
[data-testid="stSidebar"] { background: #111A35; }
[data-testid="stSidebar"] * { color: #EDF0FC; }
[data-testid="stSidebar"] hr { border-color: #35405E !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: #192441; padding: 10px 13px; margin-bottom: 5px;
    border-radius: 10px; border: 1px solid #263252;
}
h1 { color: #18213B !important; font-weight: 800 !important; letter-spacing: -1.4px; }
h2 { color: #202B4D !important; font-weight: 750 !important; }
h3 { color: #34416A !important; }
[data-testid="stMetric"] {
    background: white; padding: 19px; border-radius: 16px;
    border: 1px solid #E6E8F1; box-shadow: 0 4px 17px rgba(31,42,80,.045);
}
[data-testid="stMetricLabel"] { color: #77819A !important; font-weight: 600; }
[data-testid="stMetricValue"] { color: #594BC5 !important; font-weight: 800; }
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background: linear-gradient(110deg,#6250D3,#8368E8); color: white;
    border: none; border-radius: 11px; padding: .65rem 1.1rem; font-weight: 700;
}
.stButton > button:hover, .stFormSubmitButton > button:hover,
.stDownloadButton > button:hover { background: #4F40B7; color: white; border: none; }
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: white; border: 1px solid #DDE1EF; border-radius: 10px; color: #18213B;
}
[data-testid="stForm"] {
    background: white; padding: 24px; border-radius: 17px; border: 1px solid #E7E9F2;
}
[data-testid="stExpander"] { background: white; border: 1px solid #E6E8F1; border-radius: 13px; }
[data-testid="stDataFrame"] { border-radius: 12px; border: 1px solid #E6E8F1; overflow: hidden; }
[data-testid="stAlert"] { border-radius: 12px; }
.stProgress > div > div > div { background: linear-gradient(90deg,#6653DB,#48C9A5); }
.hero {
    background: linear-gradient(115deg,#111A35,#282C68 58%,#6352C8);
    padding: 35px; border-radius: 21px; margin-bottom: 24px;
    box-shadow: 0 12px 30px rgba(45,42,105,.15);
}
.hero-eyebrow { color: #B9ABFF; font-size: 11px; font-weight: 800; letter-spacing: 2px; }
.hero h1 { color: white !important; font-size: 35px !important; margin: 12px 0 !important; }
.hero p { color: #D7DEF6; font-size: 15px; max-width: 720px; }
.hero-status { color: #7BE0BE; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; margin-top: 15px; }
.info-card {
    background: white; padding: 20px; border-radius: 15px;
    border: 1px solid #E7E9F2; margin-bottom: 12px;
}
.info-card h4 { color: #243153; }
.info-card p { color: #73809A; font-size: 13px; }
.profile-hero {
    background: linear-gradient(120deg,#171F42,#5245A5);
    padding: 26px; border-radius: 19px; margin: 12px 0 20px;
}
.profile-hero h2 { color: white !important; }
.focus-chip { background: #FFF0F0; color: #9E3535; padding: 11px 14px; margin: 7px 0; border-radius: 10px; }
.strength-chip { background: #EAF8F2; color: #24775A; padding: 11px 14px; margin: 7px 0; border-radius: 10px; }
.allocation-card { background: white; border: 1px solid #E6E8F1; padding: 15px; border-radius: 13px; margin-bottom: 9px; }
footer, #MainMenu { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)
