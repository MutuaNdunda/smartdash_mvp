# modules/data_sources.py
import pandas as pd
import os
import streamlit as st

# Base URL pointing to your GitHub raw data folder (fallback)
BASE_URL = "https://raw.githubusercontent.com/MutuaNdunda/smartdash_mvp/refs/heads/main/data"

# Helper to load with caching
@st.cache_data
def load_csv_from_url(name: str, base_url: str = BASE_URL):
    url = f"{base_url}/{name}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        # Return empty DataFrame with a helpful message column if failed
        print(f"[load_csv_from_url] failed to load {url}: {e}")
        return pd.DataFrame()

@st.cache_data
def load_all_data():
    # Names expected in the repo — adjust if your filenames differ
    datasets = {
        "ev": "ev_adoption.csv",
        "stations": "charging_stations.csv",
        "tariffs": "tariffs.csv",
        "grid": "grid_load_week.csv",
        "sessions": "charging_sessions.csv",
        "policies": "policy_timeline.csv",
        "investment": "charging_investment.csv",
        "imports": "ev_imports.csv",
        "sectors": "sector_consumption.csv",
        "districts": "districts.csv",
        "feedback": "user_feedback.csv"
    }

    loaded = {}
    for key, fname in datasets.items():
        df = load_csv_from_url(fname)
        loaded[key] = df

    return loaded
