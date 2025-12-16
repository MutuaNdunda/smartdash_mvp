# modules/forecasting.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st

@st.cache_data
def forecast_ev_adoption(ev_df: pd.DataFrame, start_year: int = 2025, end_year: int = 2030):
    """
    Simple linear projection using historic EV_Total vs Year.
    Returns a DataFrame with Year and EV_Forecast
    """
    if {"Year", "EV_Total"}.issubset(ev_df.columns):
        X = ev_df["Year"].values.reshape(-1, 1)
        y = ev_df["EV_Total"].values
        model = LinearRegression()
        model.fit(X, y)
        future_years = np.array(range(start_year, end_year + 1)).reshape(-1, 1)
        preds = model.predict(future_years).astype(int)
        return pd.DataFrame({"Year": future_years.flatten(), "EV_Forecast": preds})
    else:
        # return empty / placeholder
        return pd.DataFrame({"Year": list(range(start_year, end_year + 1)), "EV_Forecast": [0] * (end_year - start_year + 1)})
