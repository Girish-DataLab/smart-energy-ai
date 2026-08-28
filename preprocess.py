import pandas as pd

# =========================
# DATA CLEANING FUNCTION
# =========================
def clean_data(df):
    """
    Clean and prepare dataset for ML model.

    Steps:
    1. Remove duplicates
    2. Handle missing values
    3. Convert important columns to numeric
    4. Drop invalid rows
    5. Reset index
    """
    print("[INFO] Starting data preprocessing...")

    # 1. REMOVE DUPLICATES
    df = df.drop_duplicates()

    # 2. HANDLE MISSING VALUES
    df = df.dropna()

    # 3. CONVERT IMPORTANT COLUMNS
    columns_to_convert = [
        "Global_active_power",
        "Voltage",
        "Global_intensity"
    ]

    for col in columns_to_convert:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. REMOVE INVALID VALUES
    df = df.dropna()
    df = df[(df["Voltage"] > 0) & (df["Global_intensity"] > 0)]

    # 5. RESET INDEX
    df = df.reset_index(drop=True)

    print("[SUCCESS] Data preprocessing completed.")
    return df