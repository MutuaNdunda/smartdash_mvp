# app.py
import streamlit as st
import pandas as pd
import numpy as np
import os

# Local modules
from modules.data_sources import load_all_data, BASE_URL
from modules.decision_engine import (
    compute_imbalance_score,
    recommend_siting,
    compute_grid_stress_index
)
from modules.forecasting import forecast_ev_adoption
from modules.maps import render_station_map

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="SmartDash MVP – Kigali EV Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD DATASETS (from GitHub raw or local fallback)
# ---------------------------------------------------
DATA = load_all_data()

# Unpack datasets
ev = DATA["ev"]
stations = DATA["stations"]
tariffs = DATA["tariffs"]
grid = DATA["grid"]
sessions = DATA["sessions"]
policies = DATA["policies"]
investment = DATA["investment"]
imports = DATA["imports"]
sectors = DATA["sectors"]
districts = DATA["districts"]
feedback = DATA["feedback"]

# ---------------------------------------------------
# SIDEBAR FILTERS (GLOBAL)
# ---------------------------------------------------
st.sidebar.title("Global Filters")

# Year select
if "Year" in ev.columns:
    year_selected = st.sidebar.selectbox(
        "Select Year",
        sorted(ev["Year"].unique()),
        index=len(ev["Year"].unique()) - 1
    )
else:
    year_selected = None

# District select
district_options = stations["District"].unique().tolist()
district_selected = st.sidebar.multiselect(
    "Select Districts",
    district_options,
    default=district_options
)

# Option to show data integration plan detail
show_data_integration = st.sidebar.checkbox("Show data integration notes", value=True)

# ---------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------
st.title("SmartDash MVP – Kigali EV Dashboard")
st.caption("MVP enhanced — policy decision engine, data integration plan, stakeholder co-design. (Simulated datasets)")

# ---------------------------------------------------
# TABS (core + new ones)
# ---------------------------------------------------
tabs = st.tabs([
    "Overview",
    "EV Adoption",
    "Charging Infrastructure",
    "Energy & Grid",
    "Policy & Investment",
    "Policy Decision Engine",
    "Data Integration & Sources",
    "Stakeholder Co-Design",
    "User Feedback"
])

tab_overview, tab_ev, tab_charging, tab_grid, tab_policy, tab_engine, tab_data_integ, tab_stakeholder, tab_feedback = tabs

# ===================================================
# TAB: OVERVIEW
# ===================================================
with tab_overview:
    st.header("Overview")
    col1, col2, col3, col4 = st.columns(4)

    if year_selected is not None and year_selected in ev["Year"].values:
        selected_row = ev[ev["Year"] == year_selected].iloc[-1]
        col1.metric("Total EVs", f"{int(selected_row['EV_Total']):,}")
        col2.metric("EV 2-Wheelers", f"{int(selected_row['EV_2W']):,}")
    else:
        col1.metric("Total EVs", "N/A")
        col2.metric("EV 2-Wheelers", "N/A")

    col3.metric("Charging Stations", len(stations))
    try:
        tariff_val = int(tariffs[tariffs["Tariff_Type"] == "EV_Tariff"]["Price_RWF_per_kWh"].values[0])
        col4.metric("EV Tariff (RWF/kWh)", tariff_val)
    except Exception:
        col4.metric("EV Tariff (RWF/kWh)", "N/A")

    st.subheader("EV Adoption Trend")
    if "Year" in ev.columns and "EV_Total" in ev.columns:
        st.line_chart(ev.set_index("Year")["EV_Total"])

    st.subheader("Charging Station Map")
    render_station_map(stations, district_selected)

    st.subheader("Quick Insights")
    st.write("""
    - EV growth is dominated by 2-wheelers (simulated).  
    - Charging infrastructure is concentrated in Kigali.  
    - Evening charging significantly increases grid load (simulated).  
    """)

# ===================================================
# TAB: EV ADOPTION
# ===================================================
with tab_ev:
    st.header("EV Adoption Analysis")
    if set(["Year", "EV_2W", "EV_3W", "EV_Cars", "EV_Buses"]).issubset(ev.columns):
        st.subheader("EV by Category (Annual)")
        st.line_chart(ev.set_index("Year")[["EV_2W", "EV_3W", "EV_Cars", "EV_Buses"]])
    else:
        st.write("EV category time series not available in dataset.")

    st.subheader("EV Imports (Simulated)")
    if "Year" in imports.columns and "Imported_EV_Count" in imports.columns:
        st.bar_chart(imports.set_index("Year")["Imported_EV_Count"])
    else:
        st.write("Imports data not available.")

    st.subheader("District-Level Attributes")
    st.dataframe(districts, use_container_width=True)

# ===================================================
# TAB: CHARGING INFRASTRUCTURE
# ===================================================
with tab_charging:
    st.header("Charging Infrastructure")
    st.subheader("Station Overview (sample)")
    st.dataframe(stations.head(100), use_container_width=True)

    st.subheader("Stations per District")
    st.bar_chart(stations.groupby("District").size())

    st.subheader("Charger Types")
    if "Charger_Type" in stations.columns:
        st.write(stations["Charger_Type"].value_counts())
    else:
        st.write("No charger type information.")

# ===================================================
# TAB: ENERGY & GRID
# ===================================================
with tab_grid:
    st.header("Energy Pricing & Grid Load")
    st.subheader("Energy Tariffs")
    st.dataframe(tariffs, use_container_width=True)

    st.subheader("Grid Load Curve (Daily Average)")
    if {"Hour", "Baseline_Load_kWh", "EV_Load_kWh", "Total_Load_kWh"}.issubset(grid.columns):
        daily = grid.groupby("Hour").mean().reset_index()
        st.line_chart(daily.set_index("Hour")[["Baseline_Load_kWh", "EV_Load_kWh", "Total_Load_kWh"]])
        # Grid stress index
        stress = compute_grid_stress_index(grid)
        st.subheader("Grid Stress Index (Hourly Average)")
        st.line_chart(stress)
        st.info("Higher stress values indicate hours where EV charging significantly increases load compared to baseline.")
    else:
        st.write("Grid dataset missing expected columns.")

    st.subheader("Charging Session Energy Distribution")
    if "Energy_Consumed_kWh" in sessions.columns:
        st.bar_chart(sessions["Energy_Consumed_kWh"].value_counts().head(40))
    else:
        st.write("Charging sessions data incomplete.")

    st.subheader("Electricity Consumption by Sector")
    if set(["Sector", "Annual_Consumption_GWh"]).issubset(sectors.columns):
        st.bar_chart(sectors.set_index("Sector")["Annual_Consumption_GWh"])
    else:
        st.write("Sector consumption data not available.")

# ===================================================
# TAB: POLICY & INVESTMENT
# ===================================================
with tab_policy:
    st.header("Policy Timeline & Investment Costs")
    st.subheader("Policy Timeline")
    st.dataframe(policies, use_container_width=True)
    st.subheader("Charging Investment Costs")
    st.dataframe(investment, use_container_width=True)

# ===================================================
# TAB: POLICY DECISION ENGINE (NEW)
# ===================================================
with tab_engine:
    st.header("Policy Decision Engine")
    st.write("This module translates analytics into actionable policy recommendations.")

    # 1) EV-to-Charger Imbalance Score
    if "District" in districts.columns:
        imbalance_df = compute_imbalance_score(districts, stations)
        st.subheader("EV-to-Charger Imbalance Score (EV per Charger)")
        st.dataframe(imbalance_df.sort_values("EV_per_Charger", ascending=False), use_container_width=True)

        # Priority districts
        threshold = st.slider("Imbalance threshold for high priority (EV per charger)", 10, 1000, 80)
        high_priority = imbalance_df[imbalance_df["EV_per_Charger"] > threshold]
        st.subheader("Priority Districts (Based on Threshold)")
        st.dataframe(high_priority, use_container_width=True)

        # Decision rule display
        st.info(f"Decision rule: Districts with EV_per_Charger > {threshold} are high priority for charger deployment.")
    else:
        st.write("District attributes missing for imbalance computation.")

    # 2) Siting recommendation
    st.subheader("Top Siting Recommendations (weighted score)")
    siting_reco = recommend_siting(districts, stations, top_n=8)
    st.dataframe(siting_reco, use_container_width=True)

    # 3) Investment guidance (simple)
    st.subheader("Investment Guidance (Quick heuristic)")
    if "Cost_per_Station_USD" in investment.columns:
        avg_cost = investment["Cost_per_Station_USD"].median()
        st.write(f"Median cost per charging station (sim): USD {avg_cost:,.0f}")
    else:
        st.write("Investment cost data not available.")

# ===================================================
# TAB: DATA INTEGRATION & SOURCES (NEW)
# ===================================================
with tab_data_integ:
    st.header("Data Integration & Sources")
    st.write("Plan for moving from simulated data to real institutional datasets.")

    st.subheader("Institutional Data Providers")
    st.write("""
    - **REG** → grid feeder loads, substations, distribution constraints.  
    - **RURA** → licensed charging operators, operator session logs.  
    - **MININFRA** → national EV policy & strategic targets.  
    - **City of Kigali** → traffic flow, zoning, GIS datasets.  
    - **EV Operators** → GPS trip data, station utilization data.
    """)

    st.subheader("Access Methods")
    st.write("""
    - **APIs** for near-real-time grid or tariff feeds.  
    - **CSV / SFTP** uploads for historical logs.  
    - **GIS layers** for official boundaries and transport flows.  
    - **MoUs / NDAs** for data sharing with private operators.
    """)

    st.subheader("Acquisition Timeline (example)")
    timeline = pd.DataFrame({
        "Dataset": ["Grid Load (REG)", "GPS Trip Data (Operators)", "Station Registry (RURA)", "City Traffic Flows"],
        "Access Method": ["API / CSV", "CSV API (aggregated)", "CSV / GIS", "GIS layers"],
        "Expected Timeline": ["1-3 months", "2-4 months", "1-3 months", "1-3 months"]
    })
    st.dataframe(timeline, use_container_width=True)

    if show_data_integration:
        st.markdown("**Notes:** Secure data sharing agreements early. Prototype with aggregated/ anonymized GPS data to avoid privacy issues.")

# ===================================================
# TAB: STAKEHOLDER CO-DESIGN (NEW)
# ===================================================
with tab_stakeholder:
    st.header("Stakeholder Co-Design & Pilot Plan")
    st.subheader("Who will use this dashboard?")
    st.write("""
    - MININFRA: strategic planning & policy.  
    - REG: grid integration & planning.  
    - RURA: licensing & operator registry.  
    - City of Kigali: zoning & traffic.  
    - Private EV operators: usage logs & pilot testing.
    """)

    st.subheader("Pilot Workflow")
    st.write("""
    1. Share MVP with 1–2 EV operators and City of Kigali planners.  
    2. Collect anonymized charging session logs & GPS trip aggregates.  
    3. Validate siting model and imbalance scores on real data.  
    4. Iterate: refine model weights, add new layers (e.g., socio-economic indicators).
    """)

    st.subheader("Governance & Feedback Loop")
    st.write("""
    - Quarterly stakeholder reviews.  
    - Versioned datasets and reproducible ETL.  
    - Clear channel for feedback (emails, workshops).
    """)

# ===================================================
# TAB: USER FEEDBACK
# ===================================================
with tab_feedback:
    st.header("User Feedback (Simulated)")
    colA, colB = st.columns(2)
    if {"Usability_Rating", "Clarity_Rating"}.issubset(feedback.columns):
        colA.metric("Avg Usability Rating", round(feedback["Usability_Rating"].mean(), 2))
        colB.metric("Avg Clarity Rating", round(feedback["Clarity_Rating"].mean(), 2))
    st.subheader("Responses")
    st.dataframe(feedback, use_container_width=True)

    st.subheader("Comments")
    for _, r in feedback.iterrows():
        st.write(f"- {r.get('Comments', '')}")
