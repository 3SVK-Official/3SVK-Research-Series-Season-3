import pandas as pd
from pathlib import Path

# ==========================================
# PATH
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"


# ==========================================
# 1. MODEL COMPARISON
# ==========================================

model_file = RESULTS_DIR / "model_comparison.csv"

if model_file.exists():
    model_results = pd.read_csv(model_file)

    print("\n========== MODEL COMPARISON ==========")
    print(model_results.to_string(index=False))
else:
    print("model_comparison.csv not found")


# ==========================================
# 2. BENCHMARK RESULTS
# ==========================================

benchmark_file = RESULTS_DIR / "benchmark_results.csv"

if benchmark_file.exists():
    benchmark = pd.read_csv(benchmark_file)

    print("\n========== BENCHMARK RESULTS ==========")
    print(benchmark.to_string(index=False))
else:
    print("benchmark_results.csv not found")


# ==========================================
# 3. EDGE-CLOUD RESULTS
# ==========================================

edge_file = RESULTS_DIR / "edge_cloud_comparison.csv"

if edge_file.exists():
    edge_results = pd.read_csv(edge_file)

    print("\n========== EDGE-CLOUD RESULTS ==========")

    print(
        "Total windows:",
        len(edge_results)
    )

    print(
        "Average payload reduction:",
        edge_results[
            "payload_reduction_percent"
        ].mean()
    )

    print(
        "Prediction accuracy:",
        (
            edge_results["prediction"]
            == edge_results["actual"]
        ).mean()
    )
else:
    print("edge_cloud_comparison.csv not found")


# ==========================================
# 4. SAVE SIMPLE SUMMARY
# ==========================================

summary_rows = []

if model_file.exists():

    for _, row in model_results.iterrows():

        summary_rows.append({
            "section": "Model Comparison",
            "metric": f"{row['Model']} Accuracy",
            "value": row["Accuracy"]
        })

        summary_rows.append({
            "section": "Model Comparison",
            "metric": f"{row['Model']} Precision",
            "value": row["Precision"]
        })

        summary_rows.append({
            "section": "Model Comparison",
            "metric": f"{row['Model']} Recall",
            "value": row["Recall"]
        })

        summary_rows.append({
            "section": "Model Comparison",
            "metric": f"{row['Model']} F1",
            "value": row["F1_Score"]
        })


if benchmark_file.exists():

    b = benchmark.iloc[0]

    summary_rows.append({
        "section": "Benchmark",
        "metric": "Average Latency (ms)",
        "value": b["average_latency_ms"]
    })

    summary_rows.append({
        "section": "Benchmark",
        "metric": "Process RSS Memory (MB)",
        "value": b["process_rss_memory_mb"]
    })

    summary_rows.append({
        "section": "Benchmark",
        "metric": "Theoretical Payload Reduction (%)",
        "value": b[
            "theoretical_payload_reduction_percent"
        ]
    })


if edge_file.exists():

    summary_rows.append({
        "section": "Edge-Cloud",
        "metric": "Average Payload Reduction (%)",
        "value": edge_results[
            "payload_reduction_percent"
        ].mean()
    })

    summary_rows.append({
        "section": "Edge-Cloud",
        "metric": "Prediction Accuracy",
        "value": (
            edge_results["prediction"]
            == edge_results["actual"]
        ).mean()
    })


summary_df = pd.DataFrame(summary_rows)

output_file = RESULTS_DIR / "final_results_summary.csv"

summary_df.to_csv(
    output_file,
    index=False
)

print("\n========================================")
print("FINAL RESULTS SUMMARY CREATED")
print("========================================")

print(summary_df.to_string(index=False))

print("\nSaved to:")
print(output_file)