
# **SmartDash MVP – Kigali EV Policy Dashboard**

A Minimum Viable Product (MVP) dashboard demonstrating how integrated EV, energy, and policy data can support Rwanda’s e-mobility roadmap.
This project simulates all necessary datasets and provides a working Streamlit dashboard with charts, maps, KPIs, and insight storytelling.

---

## **Project Overview**

SmartDash is a prototype digital platform designed to help policymakers, investors, and energy planners make data-driven decisions about Rwanda’s transition to electric mobility.

Because real EV datasets are not yet publicly available, this MVP uses **synthetic and proxy datasets** modeled on Rwanda and East Africa’s EV trends, charging infrastructure, energy tariffs, and grid load patterns.

The goal is to:

* Demonstrate the **architecture, visuals, and functionality** of a future national dashboard
* Showcase **policy insights, investment signals, and grid planning analytics**
* Provide a baseline for scaling into a **full production system** powered by real data from REG, RURA, RDB, and MININFRA

---

## **Project Structure**

```
smartdash_mvp/
├── data/                        # Auto-generated simulated datasets (CSV)
├── scripts/
│   └── generate_simulated_data.py   # Script to generate all synthetic data
├── dashboard/
│   └── app.py                   # Streamlit dashboard (MVP)
├── assets/                      # Images, logos (optional)
├── models/                      # Forecasting or ML models (future use)
├── venv/                        # Python virtual environment
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md
```

---

## 📊 **Datasets Included (Simulated)**

The MVP generates the following datasets using realistic Rwanda/East Africa assumptions:

1. **EV Adoption (2018–2025)**
2. **Charging Stations (180 stations, Kigali)**
3. **Energy Tariffs (REG/RURA structure)**
4. **Grid Load Profile (weekly 24×7)**
5. **Charging Session Behavior (1500+ sessions)**
6. **Policy Timeline (5 major EV-related policies)**
7. **Charging Investment & Cost Model**
8. **EV Imports (2018–2025)**
9. **Electricity Consumption by Sector**
10. **District Attributes (Gasabo, Kicukiro, Nyarugenge)**
11. **User Feedback for MVP Testing**

All files are generated into `/data/`.

---

##  **Setup Instructions**

### **1. Create a Python virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **2. Install dependencies**

```bash
pip install -r requirements.txt
```

### **3. Generate simulated datasets**

```bash
python scripts/generate_simulated_data.py
```

This will populate the `/data` directory with CSV files.

### **4. Run the dashboard**

```bash
streamlit run dashboard/app.py
```

---

##  **Dashboard Features**

The Streamlit app includes:

### **✔ Key KPI Cards**

* Total EVs
* EV 2-Wheelers
* Charging Stations Count
* EV Tariff Cost

### **✔ Charts & Visualizations**

* EV adoption trend
* Charging session energy distribution
* Grid load (baseline + EV overlay)
* Energy tariffs
* Policy timeline

### **✔ Interactive Map**

* Charging stations displayed by latitude/longitude
* Filter by district

### **✔ Insight Story Cards**

Auto-generated insights explaining:

* peak charging patterns
* charging infrastructure gaps
* tariff implications
* policy impacts

---

##  **Technology Stack**

* **Python 3**
* **Streamlit** (dashboard UI)
* **Pandas / NumPy** (data processing)
* **Plotly** (interactive charts)
* **PyDeck** (mapping)
* Optional future integrations: **S3, Snowflake, APIs**

---

## **Future Enhancements**

This MVP is built for growth. Future work will include:

* Real-time API connections (REG, RURA, MININFRA)
* National EV and charging database integration
* ROI calculators for investors
* Battery lifetime + TCO models
* Emission savings engine
* Regional/east Africa comparison data
* Production deployment on cloud (AWS, GCP, Azure)

---

##  **Author**

**Clement**
SmartDash MVP | Kigali EV Policy Dashboard
2025

