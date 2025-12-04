#----TASK 1: Data Ingestion and Validation----
import os
import pandas as pd


DATA_FOLDER = "data"
combined_data = []
log_messages = []
for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".csv"):
        file_path = os.path.join(DATA_FOLDER, filename)

        try:
            df = pd.read_csv(file_path, on_bad_lines='skip')
            name_without_ext = filename.replace(".csv", "")
            parts = name_without_ext.split("_")

            if len(parts) >= 2:
                building_name = parts[0] + "_" + parts[1]
                month = parts[-1]
            else:
                building_name = "Unknown"
                month = "Unknown"

            df["building"] = building_name
            df["month"] = month
            combined_data.append(df)

        except FileNotFoundError:
            log_messages.append(f"ERROR: File not found → {file_path}")
        except Exception as e:
            log_messages.append(f"ERROR reading {file_path}: {str(e)}")
if combined_data:
    df_combined = pd.concat(combined_data, ignore_index=True)
else:
    df_combined = pd.DataFrame()
print("\n===== Combined DataFrame Summary =====")
print(df_combined.head())
print("\nTotal rows:", len(df_combined))

# ---------- TASK 2: CORE AGGREGATION LOGIC ----------

df_combined["date"] = pd.to_datetime(df_combined["date"])

def calculate_daily_totals(df):
    daily = df.groupby("date")["consumption"].sum().reset_index()
    return daily

def calculate_weekly_aggregates(df):
    temp_df = df.set_index("date")
    weekly = temp_df["consumption"].resample("W").sum().reset_index()
    return weekly

def building_wise_summary(df):
    summary = df.groupby("building")["consumption"].agg(
        mean="mean",
        minimum="min",
        maximum="max",
        total="sum"
    ).reset_index()
    return summary

daily_totals = calculate_daily_totals(df_combined)
weekly_totals = calculate_weekly_aggregates(df_combined)
building_summary = building_wise_summary(df_combined)


print("\n===== DAILY TOTALS =====")
print(daily_totals)

print("\n===== WEEKLY TOTALS =====")
print(weekly_totals)

print("\n===== BUILDING-WISE SUMMARY =====")
print(building_summary)

#------TASK 3 : Object-Oriented Modeling----------

from datetime import datetime

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, timestamp, kwh):
        reading = MeterReading(timestamp, kwh)
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def calculate_min_consumption(self):
        if not self.meter_readings:
            return 0
        return min(r.kwh for r in self.meter_readings)

    def calculate_max_consumption(self):
        if not self.meter_readings:
            return 0
        return max(r.kwh for r in self.meter_readings)

    def calculate_mean_consumption(self):
        if not self.meter_readings:
            return 0
        return sum(r.kwh for r in self.meter_readings) / len(self.meter_readings)

    def generate_report(self):
        return {
            "building": self.name,
            "total": self.calculate_total_consumption(),
            "min": self.calculate_min_consumption(),
            "max": self.calculate_max_consumption(),
            "mean": self.calculate_mean_consumption(),
        }
class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_building(self, building_name):
        if building_name not in self.buildings:
            self.buildings[building_name] = Building(building_name)

    def add_meter_reading(self, building_name, timestamp, kwh):
        self.add_building(building_name)
        self.buildings[building_name].add_reading(timestamp, kwh)

    def generate_all_reports(self):
        reports = []
        for building in self.buildings.values():
            reports.append(building.generate_report())
        return reports

#-----TASK 4 : Visual Output with Matplotlib----------

import matplotlib.pyplot as plt

df_combined['date'] = pd.to_datetime(df_combined['date'])

daily_trend = df_combined.groupby("date")["consumption"].sum().reset_index()

df_combined['week'] = df_combined['date'].dt.isocalendar().week
weekly_avg = df_combined.groupby(["building", "week"])["consumption"].mean().reset_index()

peak_consumption = df_combined.groupby(["date", "building"])["consumption"].max().reset_index()

fig, axes = plt.subplots(3, 1, figsize=(10, 14))

axes[0].plot(daily_trend["date"], daily_trend["consumption"], marker="o")
axes[0].set_title("Daily Electricity Consumption Trend")
axes[0].set_xlabel("Date")
axes[0].set_ylabel("Consumption (kWh)")

for building in weekly_avg["building"].unique():
    b_data = weekly_avg[weekly_avg["building"] == building]
    axes[1].bar(b_data["week"], b_data["consumption"], label=building)
axes[1].set_title("Weekly Average Consumption Comparison")
axes[1].set_xlabel("Week Number")
axes[1].set_ylabel("Average Consumption")
axes[1].legend()

for building in peak_consumption["building"].unique():
    b_data = peak_consumption[peak_consumption["building"] == building]
    axes[2].scatter(b_data["date"], b_data["consumption"], label=building)
axes[2].set_title("Peak-Hour Consumption Scatter Plot")
axes[2].set_xlabel("Date")
axes[2].set_ylabel("Peak Consumption")
axes[2].legend()

plt.tight_layout()
plt.savefig("dashboard.png")
print("Dashboard image saved as dashboard.png")
plt.show()

#--------TASK 5: Persistence and Executive Summary-------

import os

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

cleaned_file_path = os.path.join(OUTPUT_FOLDER, "cleaned_energy_data.csv")
df_combined.to_csv(cleaned_file_path, index=False)

summary_file_path = os.path.join(OUTPUT_FOLDER, "building_summary.csv")
building_summary.to_csv(summary_file_path, index=False)

total_consumption = df_combined["consumption"].sum()
highest_building_row = building_summary.sort_values("total", ascending=False).iloc[0]
highest_building = highest_building_row["building"]
highest_value = highest_building_row["total"]

peak_row = df_combined.sort_values("consumption", ascending=False).iloc[0]
peak_date = peak_row["date"]
peak_kwh = peak_row["consumption"]

summary_text = (
    "----- ENERGY CONSUMPTION SUMMARY REPORT ----\n\n"
    f"Total Campus Consumption: {total_consumption} kWh\n"
    f"Highest Consuming Building: {highest_building} ({highest_value} kWh)\n"
    f"Peak Load: {peak_kwh} kWh on {peak_date}\n\n"
    "Daily Trend Observed:\n"
    "- Consumption changes over each day based on building usage patterns.\n"
    "Weekly Trend Observed:\n"
    "- Average usage varies across buildings depending on operational demand.\n\n"
    "For detailed charts, please refer to dashboard.png.\n"
)

summary_path = os.path.join(OUTPUT_FOLDER, "summary.txt")
with open(summary_path, "w") as f:
    f.write(summary_text)

print("\n---- EXECUTIVE SUMMARY----")
print(summary_text)
print("Files saved in /output folder:")
print(" cleaned_energy_data.csv")
print(" building_summary.csv")
print(" summary.txt")







