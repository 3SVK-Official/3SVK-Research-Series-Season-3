import pandas as pd
from pathlib import Path
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# ==========================================
# PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"

TEST_FILE = RESULTS_DIR / "test.csv"
MODEL_FILE = RESULTS_DIR / "random_forest_model.pkl"

# ==========================================
# LOAD DATA + MODEL
# ==========================================

test_df = pd.read_csv(TEST_FILE)
model = joblib.load(MODEL_FILE)

FEATURES = ["mean", "rms", "std", "peak"]

X_test = test_df[FEATURES]
y_test = test_df["label"]

# Prediction
y_pred = model.predict(X_test)

# ==========================================
# CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=model.classes_
)

print("========== CONFUSION MATRIX ==========")
print(cm)

# Plot confusion matrix
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

display.plot()
plt.title("Bearing Fault Classification - Confusion Matrix")
plt.tight_layout()

# Save graph
cm_file = RESULTS_DIR / "confusion_matrix.png"
plt.savefig(cm_file, dpi=300)
plt.show()

print("\nConfusion matrix saved to:")
print(cm_file)

# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance = model.feature_importances_

print("\n========== FEATURE IMPORTANCE ==========")

for feature, value in zip(FEATURES, importance):
    print(f"{feature}: {value:.6f}")

# Plot
plt.figure(figsize=(8, 5))
plt.bar(FEATURES, importance)

plt.title("Random Forest Feature Importance")
plt.xlabel("Feature")
plt.ylabel("Importance")

plt.tight_layout()

importance_file = RESULTS_DIR / "feature_importance.png"
plt.savefig(importance_file, dpi=300)
plt.show()

print("\nFeature importance graph saved to:")
print(importance_file)