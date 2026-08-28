# =========================
# ANOMALY DETECTION MODULE
# =========================

def detect_anomaly(value):
    """
    Detect abnormal energy usage based on predicted power.
    """

    try:
        value = float(value)

        # Define thresholds (can be tuned)
        if value < 0:
            return "❌ Invalid value"

        elif value < 2:
            return "Normal usage"

        elif 2 <= value < 5:
            return "Slightly high usage ⚡"

        elif 5 <= value < 8:
            return "High usage ⚠ Consider reducing load"

        else:
            return "⚠️ Anomaly detected: Extremely high energy usage"

    except Exception as e:
        return f"Error in anomaly detection: {e}"