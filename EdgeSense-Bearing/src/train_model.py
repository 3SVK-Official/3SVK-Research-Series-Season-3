import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# ==========================================
# PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"

TRAIN_FILE = RESULTS_DIR / "train.csv"
TEST_FILE = RESULTS_DIR / "test.csv"

MODEL_FILE = RESULTS_DIR / "random_forest_model.pkl"

# ==========================================
# LOAD DATA
# ==========================================

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

print("Training rows:", len(train_df))
print("Testing rows:", len(test_df))

# ==========================================
# FEATURES
# ==========================================

FEATURES = ["mean", "rms", "std", "peak"]

X_train = train_df[FEATURES]
y_train = train_df["label"]

X_test = test_df[FEATURES]
y_test = test_df["label"]

# ==========================================
# CREATE MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest...")

# ==========================================
# TRAIN
# ==========================================

model.fit(X_train, y_train)

print("Training complete!")

# ==========================================
# PREDICTION
# ==========================================

y_pred = model.predict(X_test)

# ==========================================
# EVALUATION
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n========== MODEL RESULTS ==========")

print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(model, MODEL_FILE)

print("\nModel saved to:")
print(MODEL_FILE)