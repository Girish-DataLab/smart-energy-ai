# =========================
# FUTURE PREDICTION MODULE
# =========================

import numpy as np

def future_trend(current_value):
    """
    Generate future energy prediction (simulated trend)
    """

    future_values = []

    for i in range(1, 6):
        growth = current_value * (1 + (0.05 * i))   # gradual increase
        noise = np.random.uniform(-0.1, 0.1) * current_value
        value = growth + noise
        future_values.append(round(value, 2))

    return future_values