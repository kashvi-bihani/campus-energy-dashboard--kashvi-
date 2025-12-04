#  Project Objective
The objective of this project is to analyze electricity consumption across multiple buildings and generate useful insights for energy management.  
The solution automates data ingestion, cleaning, aggregation, visualization, and reporting using Python.

---

# Methodology 
## Task 1 — Data Ingestion & Validation:
Automatically loads multiple CSV files, merges them into one DataFrame, adds metadata (building, month) & logs missing/corrupt files 
## Task 2 — Core Aggregation Logic
Computes daily totals, weekly totals, and building-wise statistics using `groupby` 
## Task 3 — OOP Modeling
Uses `Building`, `MeterReading`, and `BuildingManager` classes to model meter readings in an object-oriented design 
## Task 4 — Visualization Dashboard
 Builds 3 combined charts (trend line, bar chart, scatter plot) using Matplotlib and saves `dashboard.png` 
## Task 5 — Persistence & Reporting
Exports processed data into CSV files and generates `summary.txt` containing executive insights 

---

# Key Insights (From Analysis)
## Total campus electricity consumption 
## Highest electricity-consuming building
## Peak load: Highest recorded consumption on a specific date & time
## Trends observed:**
  - Daily usage fluctuates per building
  - Weekly averages vary depending on operational demand
- A visual dashboard combining all charts is available in `dashboard.png`

---
2. Run the script:

