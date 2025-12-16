# modules/maps.py
import streamlit as st
import pandas as pd

def render_station_map(stations_df: pd.DataFrame, selected_districts: list = None):
    """
    Standard Streamlit map rendering using stations with Latitude/Longitude columns.
    """
    df = stations_df.copy()
    lat_col = None
    lon_col = None
    for c in df.columns:
        if c.lower() in ["latitude", "lat"]:
            lat_col = c
        if c.lower() in ["longitude", "lon", "lng"]:
            lon_col = c

    if lat_col and lon_col:
        df = df.rename(columns={lat_col: "latitude", lon_col: "longitude"})
        if selected_districts:
            df = df[df["District"].isin(selected_districts)]
        st.map(df[["latitude", "longitude"]])
    else:
        st.write("Station coordinate columns not found.")
