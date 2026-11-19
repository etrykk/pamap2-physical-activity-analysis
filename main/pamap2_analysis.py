#Author: etrykk
#Date: 11/18/2026
#Project: PAMAP2 Physical Activity Data Analyzer
#Purpose: read dataset, remove invalid & missing observations
#calculate descriptive statistics, generate & save 4 graphs
#save the cleaned CSV file

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    #Read dataset
    pamap_data = pd.read_csv(DATA_DIR / "subject101.dat", sep= r"\s+", header = None)
    
    #Rename columns
    pamap_data = pamap_data.rename(columns={0: "timestamp",
                                            1: "activityID",
                                            2: "heart_rate"})
    
    #Return DataFrame
    return pamap_data

def clean_data(pamap_data):
    #Select relevant columns
    fitness_data = pamap_data[["timestamp", "activityID", "heart_rate"]].copy()
    
    #Remove missing heart rate values
    fitness_data = fitness_data.dropna(subset=["heart_rate"])
    
    #Remove activityID == 0
    fitness_data = fitness_data[fitness_data["activityID"] != 0]
    
    #Return cleaned df
    return fitness_data

def analyze_data(fitness_data):
    #Calculate descriptive statistics
    avg_heart_rate = fitness_data["heart_rate"].mean()
    max_heart_rate = fitness_data["heart_rate"].max()
    min_heart_rate = fitness_data["heart_rate"].min()
    variability = fitness_data["heart_rate"].std()
    obv_activity = fitness_data["activityID"].value_counts()
    
    #Group hr by activity
    hr_by_activity = fitness_data.groupby("activityID")["heart_rate"].mean()
    
    #Return analysis results
    return hr_by_activity, avg_heart_rate, max_heart_rate, min_heart_rate, variability, obv_activity

def visualize_data(fitness_data, hr_by_activity):
    #Histogram
    plt.figure()
    plt.hist(fitness_data["heart_rate"], bins = 20)
    plt.title("Distribution of Heart Rate Measurements")
    plt.xlabel("Heart Rate, bpm")
    plt.ylabel("Frequency")
    plt.savefig(OUTPUT_DIR / "Histogram_dist_hr.png", dpi=300, bbox_inches="tight")
    plt.show()
    
    #Bar chart
    plt.figure()
    plt.xlabel("ActivityID")
    plt.ylabel("Mean Heart Rate (bpm)")
    plt.title("Mean Heart Rate by Activity")
    plt.bar(hr_by_activity.index, hr_by_activity.values)
    plt.xticks(hr_by_activity.index)
    plt.savefig(OUTPUT_DIR / "Mean_hr_act.png", dpi=300, bbox_inches="tight")
    plt.show()
    
    #Time-series plot
    plt.figure()
    plt.xlabel("Time (seconds)")
    plt.ylabel("Heart Rate (bpm)")
    plt.title("Heart Rate by Time")
    plt.plot(fitness_data["timestamp"], fitness_data["heart_rate"])
    plt.savefig(OUTPUT_DIR / "hr_by_t.png", dpi=300, bbox_inches="tight")
    plt.show()

    #Walking vs. running box plot
    walking_data = fitness_data[fitness_data["activityID"] == 4]
    running_data = fitness_data[fitness_data["activityID"] == 5]

    plt.figure()
    plt.boxplot(
        [walking_data["heart_rate"], running_data["heart_rate"]],
        tick_labels=["Walking", "Running"]
    )
    plt.xlabel("Activity")
    plt.ylabel("Heart Rate (bpm)")
    plt.title("Heart Rate Distribution: Walking vs. Running")
    plt.savefig(OUTPUT_DIR / "hr_walking_vs_running.png", dpi=300, bbox_inches="tight")
    plt.show()
    
    
def export_data(fitness_data):
    #Save cleaned dataset to CSV
    fitness_data.to_csv(OUTPUT_DIR / "cleaned_fitness_data.csv", index=False)

def main():
    #Load dataset
    pamap_data = load_data()

    #Clean dataset
    fitness_data = clean_data(pamap_data)

    #Calculate descriptive statistics
    (hr_by_activity, avg_heart_rate, max_heart_rate,
     min_heart_rate, variability, obv_activity) = analyze_data(fitness_data)

    #Display descriptive statistics
    print(f"Average Heart Rate: {avg_heart_rate:.2f} bpm")
    print(f"Maximum Heart Rate: {max_heart_rate:.0f} bpm")
    print(f"Minimum Heart Rate: {min_heart_rate:.0f} bpm")
    print(f"Standard Deviation: {variability:.2f} bpm")
    print(f"\nMean Heart Rate by Activity:\n{hr_by_activity}")
    print(f"\nObservations by Activity:\n{obv_activity}")

    #Generate and save visualizations
    visualize_data(fitness_data, hr_by_activity)

    #Export cleaned dataset
    export_data(fitness_data)

if __name__ == "__main__":
    main()


    
    