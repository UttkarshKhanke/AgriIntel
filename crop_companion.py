import pandas as pd

COMPANION_PATH = "datasets/crop_companion.csv"

def load_companion_data():
    try:
        # Use sep=";" because your CSV uses semicolons
        df = pd.read_csv(COMPANION_PATH, sep=";")
        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()
        # Strip spaces in the crop names column
        df["crop"] = df["crop"].astype(str).str.strip().str.lower()
        return df
    except Exception as e:
        print("Error loading CSV:", e)
        return None

def get_companion_crops(crop_name):
    df = load_companion_data()
    if df is None:
        return {"error": "Could not load crop companion data."}

    if "crop" not in df.columns or "companions" not in df.columns:
        return {"error": f"CSV missing required columns. Found: {list(df.columns)}"}

    crop_name_clean = crop_name.strip().lower()
    crop_info = df[df["crop"] == crop_name_clean]

    if crop_info.empty:
        return {"error": f"No companion data available for crop '{crop_name}'"}

    companions = crop_info.iloc[0]["companions"].split(",")
    companions = [c.strip() for c in companions if c.strip()]

    notes = crop_info.iloc[0]["notes"] if "notes" in df.columns else ""

    return {"companions": companions, "notes": notes}


# Quick test
if __name__ == "__main__":
    print(get_companion_crops("Wheat"))
