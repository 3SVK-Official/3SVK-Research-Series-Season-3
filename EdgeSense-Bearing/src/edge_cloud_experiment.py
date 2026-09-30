from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import loadmat
import joblib

# ==========================================
# PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = PROJECT_DIR / "results"

MODEL_FILE = RESULTS_DIR / "random_forest_model.pkl"
TEST_FILE = RESULTS_DIR / "test.csv"

# ==========================================
# LOAD MODEL + TEST DATA
# ==========================================

model = joblib.load(MODEL_FILE)
test_df = pd.read_csv(TEST_FILE)

WINDOW_SIZE = 1000

results = []

# ==========================================
# PROCESS TEST FILES
# ==========================================

for file_name in test_df["file"].unique():

    file_path = DATA_DIR / file_name

    if not file_path.exists():
        print("Missing file:", file_name)
        continue

    data = loadmat(file_path)

    # Drive-end signal
    de_keys = [
        key for key in data.keys()
        if key.endswith("_DE_time")
    ]

    if not de_keys:
        print("No DE signal:", file_name)
        continue

    signal = data[de_keys[0]].flatten()

    file_test_rows = test_df[
        test_df["file"] == file_name
    ]

    for _, row in file_test_rows.iterrows():

        window_number = int(row["window"])

        start = (window_number - 1) * WINDOW_SIZE
        end = start + WINDOW_SIZE

        window = signal[start:end]

        if len(window) != WINDOW_SIZE:
            continue

        # ==================================
        # CLOUD PATH
        # ==================================

        # Raw data payload
        raw_payload = window.astype(
            np.float64
        ).tobytes()

        # Cloud receives raw data
        received_window = np.frombuffer(
            raw_payload,
            dtype=np.float64
        )

        # Cloud extracts features
        cloud_features = np.array([
            np.mean(received_window),
            np.sqrt(np.mean(received_window ** 2)),
            np.std(received_window),
            np.max(np.abs(received_window))
        ])

        # ==================================
        # EDGE PATH
        # ==================================

        # Edge extracts features first
        edge_features = np.array([
            np.mean(window),
            np.sqrt(np.mean(window ** 2)),
            np.std(window),
            np.max(np.abs(window))
        ])

        # Only features transmitted
        edge_payload = edge_features.astype(
            np.float64
        ).tobytes()

        # ==================================
        # PAYLOAD COMPARISON
        # ==================================

        raw_bytes = len(raw_payload)
        feature_bytes = len(edge_payload)

        reduction = (
            1 - feature_bytes / raw_bytes
        ) * 100

        # ==================================
        # PREDICTION
        # ==================================

        prediction = model.predict(
            edge_features.reshape(1, -1)
        )[0]

        results.append({
            "file": file_name,
            "window": window_number,
            "raw_bytes": raw_bytes,
            "feature_bytes": feature_bytes,
            "payload_reduction_percent": reduction,
            "prediction": prediction,
            "actual": row["label"]
        })


# ==========================================
# SAVE RESULTS
# ==========================================

results_df = pd.DataFrame(results)

output_file = (
    RESULTS_DIR /
    "edge_cloud_comparison.csv"
)

results_df.to_csv(
    output_file,
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

print("\n================================")
print("EDGE-CLOUD EXPERIMENT COMPLETE")
print("================================")

print(
    "Total windows:",
    len(results_df)
)

if len(results_df) > 0:

    print(
        "Raw payload per window:",
        results_df["raw_bytes"].iloc[0],
        "bytes"
    )

    print(
        "Feature payload per window:",
        results_df["feature_bytes"].iloc[0],
        "bytes"
    )

    print(
        "Average payload reduction:",
        results_df[
            "payload_reduction_percent"
        ].mean(),
        "%"
    )

    print(
        "Prediction accuracy:",
        (
            results_df["prediction"]
            == results_df["actual"]
        ).mean()
    )

print("\nSaved to:")
print(output_file)

print(
    "\nNOTE: This is a local emulation of "
    "edge/cloud data flow. It does not measure "
    "real network latency."
)