import time
import os
from pathlib import Path

import joblib
import pandas as pd
import psutil


# ==========================================
# PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"

MODEL_FILE = RESULTS_DIR / "random_forest_model.pkl"
TEST_FILE = RESULTS_DIR / "test.csv"


# ==========================================
# LOAD MODEL + DATA
# ==========================================

model = joblib.load(MODEL_FILE)
test_df = pd.read_csv(TEST_FILE)

FEATURES = ["mean", "rms", "std", "peak"]

X_test = test_df[FEATURES]


# ==========================================
# PROCESS INFORMATION
# ==========================================

process = psutil.Process(os.getpid())


# ==========================================
# MODEL PREDICTION
# ==========================================

start_time = time.perf_counter()

predictions = model.predict(X_test)

end_time = time.perf_counter()

total_time = end_time - start_time

average_latency_ms = (
    total_time / len(X_test)
) * 1000


# ==========================================
# MEMORY
# ==========================================

memory_mb = (
    process.memory_info().rss
    / (1024 * 1024)
)


# ==========================================
# DATA PAYLOAD
# ==========================================

raw_samples = 1000
bytes_per_value = 8

raw_bytes = raw_samples * bytes_per_value

feature_count = 4

feature_bytes = feature_count * bytes_per_value

payload_reduction = (
    (1 - feature_bytes / raw_bytes) * 100
)


# ==========================================
# RESULTS
# ==========================================

print("\n========== BENCHMARK RESULTS ==========")

print("Test samples:", len(X_test))

print(
    "Total inference time:",
    total_time,
    "seconds"
)

print(
    "Average inference latency:",
    average_latency_ms,
    "milliseconds"
)

print(
    "Process RSS memory:",
    memory_mb,
    "MB"
)

print("\n========== DATA PAYLOAD ==========")

print(
    "Raw window:",
    raw_bytes,
    "bytes"
)

print(
    "Feature payload:",
    feature_bytes,
    "bytes"
)

print(
    "Theoretical payload reduction:",
    payload_reduction,
    "%"
)


# ==========================================
# SAVE BENCHMARK RESULTS
# ==========================================

benchmark_results = pd.DataFrame([{
    "test_samples": len(X_test),
    "total_inference_seconds": total_time,
    "average_latency_ms": average_latency_ms,
    "process_rss_memory_mb": memory_mb,
    "raw_window_bytes": raw_bytes,
    "feature_payload_bytes": feature_bytes,
    "theoretical_payload_reduction_percent": payload_reduction
}])

output_file = RESULTS_DIR / "benchmark_results.csv"

benchmark_results.to_csv(
    output_file,
    index=False
)

print("\nSaved benchmark results to:")
print(output_file)