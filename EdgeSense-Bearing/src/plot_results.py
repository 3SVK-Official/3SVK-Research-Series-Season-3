import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# ==========================================
# PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"

INPUT_FILE = RESULTS_DIR / "model_comparison.csv"

# ==========================================
# LOAD RESULTS
# ==========================================

df = pd.read_csv(INPUT_FILE)

print("Model comparison:")
print(df)

# ==========================================
# METRIC GRAPH
# ==========================================

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1_Score"
]

for metric in metrics:

    plt.figure(figsize=(9, 5))

    plt.bar(df["Model"], df[metric])

    plt.title(f"{metric} Comparison")
    plt.xlabel("Model")
    plt.ylabel(metric)

    plt.xticks(rotation=20)
    plt.ylim(0, 1)
    plt.tight_layout()

    output_file = RESULTS_DIR / f"{metric.lower()}_comparison.png"

    plt.savefig(output_file, dpi=300)

    print(f"Saved: {output_file}")

    plt.show()