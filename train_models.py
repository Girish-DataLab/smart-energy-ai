import os
import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from preprocess import clean_data

# Base directory for reliable path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# =========================
# LOAD DATASET
# =========================
full_data_path = os.path.join(BASE_DIR, "data.csv")
sample_data_path = os.path.join(BASE_DIR, "data_sample.csv")

data_file = full_data_path if os.path.exists(full_data_path) else sample_data_path
print(f"[INFO] Loading dataset from {os.path.basename(data_file)}...")
data = pd.read_csv(data_file)

# =========================
# REDUCE DATA SIZE (FAST TRAINING)
# =========================
sample_size = min(5000, len(data))
if len(data) > sample_size:
    print(f"[INFO] Sampling {sample_size} records for fast training...")
    data = data.sample(sample_size, random_state=42)

# =========================
# CLEAN DATA
# =========================
print("[INFO] Cleaning data...")
data = clean_data(data)

# =========================
# CONVERT COLUMNS TO NUMERIC
# =========================
print("[INFO] Converting columns to numeric...")
cols = ["Global_active_power", "Voltage", "Global_intensity"]

for col in cols:
    if col in data.columns:
        data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna()

# =========================
# FEATURE SELECTION
# =========================
print("[INFO] Selecting features...")
X = data[["Voltage", "Global_intensity"]]
y = data["Global_active_power"]

# =========================
# TRAIN TEST SPLIT
# =========================
print("[INFO] Splitting dataset into train/test...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# MODELS (OPTIMIZED)
# =========================
print("[INFO] Initializing models...")
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=10, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=50, random_state=42),
}

results = {}

# =========================
# TRAIN + EVALUATE
# =========================
print("[INFO] Training models...")
for name, model in models.items():
    print(f"  -> Training {name}...")
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    # Save model
    filename = name.lower().replace(" ", "_") + ".pkl"
    joblib.dump(model, os.path.join(MODELS_DIR, filename))

    results[name] = {
        "MAE": round(mae, 3),
        "R2": round(r2, 3),
    }

# =========================
# SAVE METRICS
# =========================
metrics_df = pd.DataFrame(results).T
metrics_df.to_csv(os.path.join(MODELS_DIR, "model_metrics.csv"))

# =========================
# OUTPUT
# =========================
print("\n[SUCCESS] Models trained successfully!\n")
print(metrics_df)