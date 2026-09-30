import pandas as pd
from pathlib import Path

# ==========================================
# DATASET PATH
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_DIR / "results" / "feature_dataset.csv"

# CSV read karo
dataset = pd.read_csv(CSV_FILE)


# ==========================================
# BASIC INFORMATION
# ==========================================

print("========== DATASET INFORMATION ==========")

print("Number of rows:", len(dataset))
print("Number of columns:", len(dataset.columns))

print("\nColumns:")
print(dataset.columns.tolist())


# ==========================================
# FIRST 5 ROWS
# ==========================================

print("\n========== FIRST 5 ROWS ==========")
print(dataset.head())


# ==========================================
# CLASS DISTRIBUTION
# ==========================================

print("\n========== CLASS DISTRIBUTION ==========")
print(dataset["label"].value_counts())


# ==========================================
# MISSING VALUES
# ==========================================

print("\n========== MISSING VALUES ==========")
print(dataset.isnull().sum())