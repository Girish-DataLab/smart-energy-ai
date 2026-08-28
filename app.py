import os
import csv
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file

# ML modules
from ml_service import load_models, get_best_prediction, generate_smart_tip, calculate_carbon
from anomaly import detect_anomaly
from future_predict import future_trend

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "energy_secret")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "history.csv")

# Load models
try:
    models = load_models()
    print("[SUCCESS] Models loaded successfully")
except Exception as e:
    print("[ERROR] Model loading failed:", e)
    models = None

RATE_PER_UNIT = 7


# =========================
# LOGIN SYSTEM
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Configurable admin credentials
        admin_user = os.environ.get("ADMIN_USER", "admin")
        admin_pass = os.environ.get("ADMIN_PASS", "1234")

        if username == admin_user and password == admin_pass:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


# =========================
# SAVE HISTORY
# =========================
def save_history(voltage, intensity, prediction, bill):
    file_exists = os.path.isfile(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        # Write header only once
        if not file_exists:
            writer.writerow(["Voltage", "Intensity", "Prediction", "Bill"])
        writer.writerow([voltage, intensity, prediction, bill])


# =========================
# API: PREDICT
# =========================
@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        if models is None:
            return jsonify({"error": "Models not loaded"})

        data = request.get_json()

        voltage = float(data["voltage"])
        intensity = float(data["intensity"])

        input_data = [[voltage, intensity]]

        results, best_model = get_best_prediction(models, input_data)
        prediction = results[best_model]

        bill = prediction * RATE_PER_UNIT
        carbon = calculate_carbon(prediction)
        tip = generate_smart_tip(prediction)
        anomaly = detect_anomaly(prediction)
        future = future_trend(prediction)

        # Save history
        save_history(voltage, intensity, round(prediction, 2), round(bill, 2))

        return jsonify({
            "prediction": round(prediction, 2),
            "bill": round(bill, 2),
            "carbon": carbon,
            "tip": tip,
            "anomaly": anomaly,
            "best_model": best_model,
            "future": future
        })

    except Exception as e:
        print("[ERROR] PREDICT ERROR:", e)
        return jsonify({"error": str(e)})


# =========================
# API: HISTORY
# =========================
@app.route("/api/history")
def history():
    try:
        if not os.path.exists(HISTORY_FILE):
            return jsonify([])

        df = pd.read_csv(HISTORY_FILE)

        if df.empty or "Prediction" not in df.columns:
            return jsonify([])

        return jsonify(df["Prediction"].tail(10).tolist())

    except Exception as e:
        print("[ERROR] HISTORY ERROR:", e)
        return jsonify([])


# =========================
# DOWNLOAD REPORT
# =========================
@app.route("/download")
def download():
    if os.path.exists(HISTORY_FILE):
        return send_file(HISTORY_FILE, as_attachment=True)
    return "No report found"


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)