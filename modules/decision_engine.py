# modules/decision_engine.py
import pandas as pd
import numpy as np

def compute_imbalance_score(districts_df: pd.DataFrame, stations_df: pd.DataFrame):
    """
    Compute EV per charger by district.
    districts_df should contain a column 'District' and an EV population column if available (e.g., 'EV_Population' or 'EV_Total').
    stations_df should contain 'District' entries for each station.
    """
    # station counts
    station_counts = stations_df.groupby("District").size().rename("Station_Count").reset_index()
    # EV counts from districts table - try multiple possible names
    ev_col = None
    for c in ["EV_Population", "EV_Total", "EV_Estimate"]:
        if c in districts_df.columns:
            ev_col = c
            break

    merged = districts_df.copy()
    if ev_col is None:
        # If there's no EV column, create a placeholder using population if available
        if "Population" in merged.columns:
            merged["EV_Population"] = (merged["Population"] * 0.01).astype(int)  # assume 1% EV for placeholder
            ev_col = "EV_Population"
        else:
            merged["EV_Population"] = 0
            ev_col = "EV_Population"

    merged = merged.merge(station_counts, on="District", how="left").fillna({"Station_Count": 0})
    # avoid division by zero
    merged["EV_per_Charger"] = merged[ev_col] / merged["Station_Count"].replace(0, np.nan)
    merged["EV_per_Charger"] = merged["EV_per_Charger"].fillna(merged[ev_col])  # if no station, just EV count
    return merged[["District", ev_col, "Station_Count", "EV_per_Charger"]].rename(columns={ev_col: "EV_Population"})

def recommend_siting(districts_df: pd.DataFrame, stations_df: pd.DataFrame, top_n: int = 5):
    """
    Simple weighted scoring combining EV population, traffic flow, and grid capacity indices.
    Expects columns in districts_df: 'District', 'EV_Population' or similar, 'Traffic_Flow_Index', 'Grid_Capacity_Index'
    """
    df = districts_df.copy()
    # Ensure columns exist - create defaults
    if "EV_Population" not in df.columns:
        df["EV_Population"] = df.get("Population", 0) * 0.01  # fallback
    if "Traffic_Flow_Index" not in df.columns:
        df["Traffic_Flow_Index"] = df.get("Traffic", 1)
    if "Grid_Capacity_Index" not in df.columns:
        df["Grid_Capacity_Index"] = df.get("GridCapacity", 1)

    # Normalize components
    for col in ["EV_Population", "Traffic_Flow_Index", "Grid_Capacity_Index"]:
        if df[col].max() > 0:
            df[f"{col}_norm"] = df[col] / df[col].max()
        else:
            df[f"{col}_norm"] = 0

    # Weighted score - tweakable
    df["Score"] = 0.5 * df["EV_Population_norm"] + 0.3 * df["Traffic_Flow_Index_norm"] + 0.2 * df["Grid_Capacity_Index_norm"]
    return df.sort_values("Score", ascending=False)[["District", "EV_Population", "Traffic_Flow_Index", "Grid_Capacity_Index", "Score"]].head(top_n)

def compute_grid_stress_index(grid_df):
    """
    Compute a simple stress index: (Total_Load / Baseline_Load) * 100
    Returns a Series indexed by Hour.
    """
    if {"Hour", "Baseline_Load_kWh", "Total_Load_kWh"}.issubset(grid_df.columns):
        hourly = grid_df.groupby("Hour").mean()
        stress = (hourly["Total_Load_kWh"] / hourly["Baseline_Load_kWh"]) * 100
        stress = stress.fillna(0)
        stress.index.name = "Hour"
        return stress
    else:
        return pd.Series([])
