from scipy.io import loadmat
from pathlib import Path
import numpy as np
import pandas as pd

# ==========================================
# PATHS
# ==========================================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

RESULTS_DIR.mkdir(exist_ok=True)

# ==========================================
# FILE LABEL MAPPING
# ==========================================

FILE_LABELS = {
    "97.mat": "Normal",
    "98.mat": "Normal",
    "99.mat": "Normal",
    "100.mat": "Normal",

    "105.mat": "Inner_Race",
    "106.mat": "Inner_Race",
    "107.mat": "Inner_Race",
    "108.mat": "Inner_Race",

    "118.mat": "Ball",
    "119.mat": "Ball",
    "120.mat": "Ball",
    "121.mat": "Ball",

    "130.mat": "Outer_Race",
    "131.mat": "Outer_Race",
    "132.mat": "Outer_Race",
    "133.mat": "Outer_Race",
}

# ==========================================
# SETTINGS
# ==========================================

WINDOW_SIZE = 1000

rows = []

print("Starting dataset creation...\n")

# ==========================================
# PROCESS EVERY FILE
# ==========================================

for file_name, label in FILE_LABELS.items():

    file_path = DATA_DIR / file_name

    if not file_path.exists():
        print(f"WARNING: {file_name} not found")
        continue

    print(f"Processing: {file_name} -> {label}")

    data = loadmat(file_path)

    # DE vibration variable find karo
    de_keys = [key for key in data.keys() if key.endswith("_DE_time")]

    if not de_keys:
        print(f"  ERROR: DE vibration signal not found in {file_name}")
        continue

    signal = data[de_keys[0]].flatten()

    total_windows = len(signal) // WINDOW_SIZE

    # Har window ko feature row banao
    for i in range(total_windows):

        start = i * WINDOW_SIZE
        end = start + WINDOW_SIZE

        window = signal[start:end]

        mean = np.mean(window)
        rms = np.sqrt(np.mean(window ** 2))
        std = np.std(window)
        peak = np.max(np.abs(window))

        rows.append({
            "file": file_name,
            "label": label,
            "window": i + 1,
            "mean": mean,
            "rms": rms,
            "std": std,
            "peak": peak
        })


# ==========================================
# SAVE CSV
# ==========================================

dataset = pd.DataFrame(rows)

output_file = RESULTS_DIR / "feature_dataset.csv"

dataset.to_csv(output_file, index=False)

print("\n================================")
print("DATASET CREATION COMPLETE")
print("================================")

print("Total rows:", len(dataset))
print("Total columns:", len(dataset.columns))

print("\nClass distribution:")
print(dataset["label"].value_counts())

print("\nSaved to:")
print(output_file)