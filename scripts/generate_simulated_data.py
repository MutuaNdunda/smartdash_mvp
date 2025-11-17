import pandas as pd
import numpy as np
import os

# Output directory
BASE_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

print(f"Writing simulated datasets to: {OUT_DIR}")

# --------------------------------------------------
# 1. EV Adoption Dataset
# --------------------------------------------------
years = list(range(2018, 2026))

ev_adoption = pd.DataFrame({
    "Year": years,
    "EV_2W": np.random.randint(300, 6000, len(years)).cumsum(),
    "EV_3W": np.random.randint(50, 800, len(years)).cumsum(),
    "EV_Cars": np.random.randint(20, 250, len(years)).cumsum(),
    "EV_Buses": np.random.randint(1, 15, len(years)).cumsum()
})

ev_adoption["EV_Total"] = ev_adoption[["EV_2W","EV_3W","EV_Cars","EV_Buses"]].sum(axis=1)
ev_adoption["YoY_Growth_%"] = ev_adoption["EV_Total"].pct_change().fillna(0) * 100

ev_adoption.to_csv(os.path.join(OUT_DIR, "ev_adoption.csv"), index=False)


# --------------------------------------------------
# 2. Charging Stations Dataset
# --------------------------------------------------
n_stations = 180

charging_stations = pd.DataFrame({
    "Station_ID": range(1, n_stations + 1),
    "Station_Name": [f"Station_{i}" for i in range(1, n_stations + 1)],
    "Latitude": np.random.uniform(-1.98, -1.90, n_stations),
    "Longitude": np.random.uniform(30.00, 30.15, n_stations),
    "District": np.random.choice(["Gasabo", "Kicukiro", "Nyarugenge"], n_stations),
    "Charger_Type": np.random.choice(["AC", "DC_Fast", "Swap"], n_stations, p=[0.2, 0.05, 0.75]),
    "Charging_Speed_kW": np.random.choice([3.3, 7, 22, 50], n_stations),
    "Ports": np.random.randint(1, 8, n_stations),
    "Operator": np.random.choice(["Ampersand", "RwandaEV", "Inex", "E-Mobility"], n_stations),
    "Year_Installed": np.random.randint(2018, 2026, n_stations)
})

charging_stations.to_csv(os.path.join(OUT_DIR, "charging_stations.csv"), index=False)


# --------------------------------------------------
# 3. Tariffs / Energy Pricing Dataset
# --------------------------------------------------
tariffs = pd.DataFrame({
    "Tariff_Type": ["Residential", "Commercial", "Industrial", "EV_Tariff"],
    "Price_RWF_per_kWh": [280, 230, 180, 150],
    "Peak_Hours": ["18:00-22:00"] * 4,
    "Offpeak_Hours": ["00:00-05:00"] * 4
})

tariffs.to_csv(os.path.join(OUT_DIR, "tariffs.csv"), index=False)


# --------------------------------------------------
# 4. Grid Load Profile Dataset (Weekly)
# --------------------------------------------------
rows = []
for day in range(7):  # 7 days
    for hour in range(24):
        baseline = int(np.random.normal(180, 35))
        ev_load = int(np.random.choice([0, 2, 5, 8, 12, 15, 20], p=[0.15,0.2,0.25,0.15,0.1,0.1,0.05]))
        rows.append({
            "Day": day,
            "Hour": hour,
            "Baseline_Load_kWh": baseline,
            "EV_Load_kWh": ev_load,
            "Total_Load_kWh": baseline + ev_load
        })

grid_load = pd.DataFrame(rows)
grid_load.to_csv(os.path.join(OUT_DIR, "grid_load_week.csv"), index=False)


# --------------------------------------------------
# 5. Charging Session Behavior Dataset
# --------------------------------------------------
n_sessions = 1500

charging_sessions = pd.DataFrame({
    "Session_ID": range(1, n_sessions + 1),
    "Vehicle_Type": np.random.choice(["2W", "3W", "Car", "Bus"], n_sessions, p=[0.7, 0.1, 0.18, 0.02]),
    "Energy_Consumed_kWh": np.round(np.random.uniform(0.3, 25, n_sessions), 2),
    "Start_Hour": np.random.randint(0, 24, n_sessions),
    "Duration_min": np.random.randint(10, 240, n_sessions),
    "Charging_Location": np.random.choice(["Home", "Public", "Work", "Swap"], n_sessions, p=[0.4, 0.35, 0.15, 0.1])
})

charging_sessions["End_Hour"] = (charging_sessions["Start_Hour"] + charging_sessions["Duration_min"] / 60) % 24
charging_sessions.to_csv(os.path.join(OUT_DIR, "charging_sessions.csv"), index=False)


# --------------------------------------------------
# 6. Policy Timeline Dataset
# --------------------------------------------------
policy_timeline = pd.DataFrame({
    "Policy_Name": [
        "EV Import Tax Exemption",
        "EV Charging Tariff Reform",
        "National EV Strategy",
        "EV Public Transport Pilot",
        "Battery Swap Regulation"
    ],
    "Year": [2019, 2020, 2021, 2023, 2024],
    "Impact_Description": [
        "Boosted EV imports",
        "Lower charging costs",
        "National roadmap established",
        "Pilot for electric buses",
        "Regulation for battery swap networks"
    ]
})

policy_timeline.to_csv(os.path.join(OUT_DIR, "policy_timeline.csv"), index=False)


# --------------------------------------------------
# 7. Charging Investment Dataset
# --------------------------------------------------
charging_investment = pd.DataFrame({
    "Charger_Type": ["AC", "DC_Fast", "Swap"],
    "CapEx_RWF": [5000000, 30000000, 15000000],
    "Installation_Cost_RWF": [1000000, 7000000, 3000000],
    "OM_Cost_RWF_per_year": [200000, 800000, 500000],
    "Average_Utilization_pct": [30, 50, 70]
})

charging_investment.to_csv(os.path.join(OUT_DIR, "charging_investment.csv"), index=False)


# --------------------------------------------------
# 8. EV Imports Dataset
# --------------------------------------------------
ev_imports = pd.DataFrame({
    "Year": years,
    "Imported_EV_Count": np.random.randint(50, 500, len(years)).cumsum(),
    "Imported_ICE_Count": np.random.randint(2000, 5000, len(years))
})

ev_imports.to_csv(os.path.join(OUT_DIR, "ev_imports.csv"), index=False)


# --------------------------------------------------
# 9. Electricity Consumption by Sector Dataset
# --------------------------------------------------
sector_consumption = pd.DataFrame({
    "Sector": ["Residential", "Commercial", "Industrial", "Transport"],
    "Annual_Consumption_GWh": [750, 300, 900, 12]
})

sector_consumption.to_csv(os.path.join(OUT_DIR, "sector_consumption.csv"), index=False)


# --------------------------------------------------
# 10. District Attributes Dataset
# --------------------------------------------------
districts = pd.DataFrame({
    "District": ["Gasabo", "Kicukiro", "Nyarugenge"],
    "Population": [800000, 500000, 350000],
    "Road_Length_km": [600, 450, 300]
})

districts.to_csv(os.path.join(OUT_DIR, "districts.csv"), index=False)


# --------------------------------------------------
# 11. User Feedback Dataset
# --------------------------------------------------
# --------------------------------------------------
# 11. User Feedback Dataset
# --------------------------------------------------
n_feedback = 200

user_feedback = pd.DataFrame({
    "User_ID": range(1, n_feedback + 1),
    "User_Type": np.random.choice(["Policy", "Investor", "Engineer"], n_feedback),
    "Usability_Rating": np.random.randint(1, 6, n_feedback),
    "Clarity_Rating": np.random.randint(1, 6, n_feedback),
    "Comments": np.random.choice([
        # Policy User Comments
        "The policy impact visualization lacks granular district-level data needed for targeted interventions and equitable resource allocation",
        "Missing integration with national development goals makes it difficult to align EV infrastructure planning with broader economic strategies",
        "The subsidy modeling tool doesn't account for varying income levels across regions, limiting its effectiveness for social equity analysis",
        "Environmental impact metrics are oversimplified and don't include lifecycle emissions or battery production environmental costs",
        "Public health co-benefits from reduced air pollution are not quantified, making cost-benefit analysis incomplete for policy justification",
        
        # Investor User Comments
        "ROI calculations lack sensitivity analysis for key variables like electricity price fluctuations and changing adoption rates",
        "The investment risk assessment doesn't incorporate regulatory changes or potential policy shifts over the 5-10 year horizon",
        "Missing comparative analysis between different charger types makes capital allocation decisions difficult without external tools",
        "The demand forecasting model doesn't differentiate between urban, peri-urban, and rural adoption patterns across Rwanda",
        "Operating cost projections are static and don't account for maintenance escalation or technological obsolescence risks",
        
        # Engineer User Comments
        "Grid impact simulations need more granular time-step analysis (15-minute intervals instead of hourly) for proper infrastructure planning",
        "The API documentation is incomplete and lacks examples for integrating real-time charging station status with third-party applications",
        "Battery degradation models are oversimplified and don't account for different chemistry types or charging patterns impact on lifespan",
        "The load forecasting algorithm doesn't consider seasonal variations or special events that significantly impact electricity demand",
        "Missing interoperability standards between different charger manufacturers creates integration challenges at the network level",
        
        # General Usability Comments
        "The filter system becomes unresponsive when applying multiple criteria to large datasets, requiring page refresh to restore functionality",
        "Export functionality is limited to CSV format; we need PDF reports with customizable layouts for executive presentations",
        "Real-time data updates are inconsistent across dashboard components, causing confusion when different panels show conflicting numbers",
        "The mobile interface lacks critical functionality available on desktop, particularly for map-based data exploration and filtering",
        "User permission system is too basic - we need role-based access control with customizable data visibility for different team members",
        
        # Data Quality Comments
        "Charging station utilization data shows implausible patterns suggesting either reporting errors or data processing issues",
        "The vehicle range data appears outdated and doesn't reflect improvements in newer EV models entering the Rwandan market",
        "Energy consumption metrics don't correlate with actual billing data from utility providers, indicating calibration problems",
        "Historical data has significant gaps during 2020-2021 period, limiting trend analysis and long-term performance assessment",
        "Geospatial coordinates for some charging stations are inaccurate, placing them in residential buildings instead of actual locations",
        
        # Feature Requests
        "Need predictive analytics for optimal charger placement based on traffic patterns, population density, and existing infrastructure",
        "Integration with renewable energy generation data would help optimize charging schedules for maximum clean energy utilization",
        "Customizable alert system for abnormal charging patterns, equipment failures, or significant deviations from forecasted demand",
        "Benchmarking tools to compare performance metrics against international standards and similar markets in the region",
        "Scenario planning module to model different adoption curves, policy interventions, and technology disruption scenarios"
    ], n_feedback)
})

user_feedback.to_csv(os.path.join(OUT_DIR, "user_feedback.csv"), index=False)