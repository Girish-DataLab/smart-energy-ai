import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# =========================
# LOAD ALL MODELS
# =========================
def load_models():
    try:
        models = {
            "Linear Regression": joblib.load(os.path.join(MODELS_DIR, "linear_regression.pkl")),
            "Random Forest": joblib.load(os.path.join(MODELS_DIR, "random_forest.pkl")),
            "Gradient Boosting": joblib.load(os.path.join(MODELS_DIR, "gradient_boosting.pkl")),
        }
        print("[SUCCESS] All models loaded successfully")
        return models
    except Exception as e:
        print("[ERROR] Error loading models:", e)
        return None


# =========================
# MULTI-MODEL PREDICTION
# =========================
def get_best_prediction(models, input_data):
    results = {}

    # Run prediction using all models
    for name, model in models.items():
        try:
            pred = model.predict(input_data)[0]
            results[name] = float(pred)
        except Exception as e:
            print(f"[ERROR] Prediction error in {name}: {e}")
            results[name] = 0.0

    # =========================
    # SELECT BEST MODEL BASED ON R²
    # =========================
    try:
        metrics_path = os.path.join(MODELS_DIR, "model_metrics.csv")
        metrics = pd.read_csv(metrics_path, index_col=0)
        best_model = metrics["R2"].idxmax()
    except Exception as e:
        print("[WARN] Could not load metrics, using fallback:", e)
        best_model = max(results, key=results.get)

    return results, best_model


# =========================
# SMART RECOMMENDATION SYSTEM
# =========================
def generate_smart_tip(usage):
    if usage < 1.5:
        return "Efficient usage. Keep it up!"
    elif 1.5 <= usage < 3:
        return "Moderate usage. Try reducing peak-time appliances."
    elif 3 <= usage < 6:
        return "High usage. Consider optimizing appliances and AC usage."
    else:
        return "Very high usage! Immediate reduction needed."


# =========================
# CARBON FOOTPRINT CALCULATION
# =========================
def calculate_carbon(usage):
    # Approximate conversion: 1 kWh ≈ 0.82 kg CO₂
    carbon = usage * 0.82
    return round(carbon, 2)