import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedGroupKFold

# ==========================================
# PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "results" / "feature_dataset.csv"
RESULTS_DIR = PROJECT_DIR / "results"

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(INPUT_FILE)

print("Original dataset rows:", len(df))

# ==========================================
# FEATURES / LABEL / GROUP
# ==========================================

X = df[["mean", "rms", "std", "peak"]]

y = df["label"]

# Same file ki windows ek hi group mein rahengi
groups = df["file"]

# ==========================================
# STRATIFIED GROUP SPLIT
# ==========================================

splitter = StratifiedGroupKFold(
    n_splits=4,
    shuffle=True,
    random_state=42
)

# Pehla fold use karenge
train_idx, test_idx = next(
    splitter.split(X, y, groups=groups)
)

train_df = df.iloc[train_idx].copy()
test_df = df.iloc[test_idx].copy()

# ==========================================
# SAVE
# ==========================================

train_file = RESULTS_DIR / "train.csv"
test_file = RESULTS_DIR / "test.csv"

train_df.to_csv(train_file, index=False)
test_df.to_csv(test_file, index=False)

# ==========================================
# RESULTS
# ==========================================

print("\n========== SPLIT COMPLETE ==========")

print("Training rows:", len(train_df))
print("Testing rows:", len(test_df))

print("\nTraining classes:")
print(train_df["label"].value_counts())

print("\nTesting classes:")
print(test_df["label"].value_counts())

print("\nTraining files:")
print(sorted(train_df["file"].unique()))

print("\nTesting files:")
print(sorted(test_df["file"].unique()))

print("\nSaved:")
print(train_file)
print(test_file)