import os
import pickle
import pandas as pd

# Paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "water_fertilizer_model.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "crop_water_fertilizer_plan.csv")

# Load trained ML model and encoders
with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

model = data["model"]
crop_encoder = data["crop_encoder"]
irrigation_encoder = data["irrigation_encoder"]
notes_encoder = data["notes_encoder"]

# Load CSV knowledge base
crop_df = pd.read_csv(DATA_PATH)


def get_water_fertilizer_plan(crop_name: str, soil_N: int, soil_P: int, soil_K: int):
    """
    Generate fertilizer + water planning for a given crop.
    Uses ML model to predict irrigation type and CSV for fertilizer recommendations.
    """

    # Find crop in CSV
    crop_info = crop_df[crop_df["Crop"].str.lower() == crop_name.lower()]
    if crop_info.empty:
        return {"error": f"No fertilizer data available for crop '{crop_name}'"}

    # Take first matching row
    crop_row = crop_info.iloc[0]
    recommended_N, recommended_P, recommended_K = crop_row["N"], crop_row["P"], crop_row["K"]

    # Compute nutrient gaps
    gap_N = max(0, recommended_N - soil_N)
    gap_P = max(0, recommended_P - soil_P)
    gap_K = max(0, recommended_K - soil_K)

    # Encode crop name for model
    crop_encoded = crop_encoder.transform([crop_name])[0]

    # Predict irrigation type using model
    irrigation_pred_encoded = model.predict([[crop_encoded, soil_N, soil_P, soil_K, ph]])[0]
    irrigation_type = irrigation_encoder.inverse_transform([irrigation_pred_encoded])[0]

    # Decode recommended notes
    notes_encoded = crop_row["Notes"]
    # Optional: you can directly use Notes from CSV instead of decoding ML output
    # decoded_notes = notes_encoder.inverse_transform([notes_encoded])[0]

    plan = {
        "crop": crop_name,
        "recommended_NPK": {
            "N": recommended_N,
            "P": recommended_P,
            "K": recommended_K
        },
        "soil_NPK": {
            "N": soil_N,
            "P": soil_P,
            "K": soil_K
        },
        "nutrient_gaps": {
            "N": gap_N,
            "P": gap_P,
            "K": gap_K
        },
        "irrigation": irrigation_type,
        "notes": crop_row["Notes"]
    }

    return plan


# Quick test
if __name__ == "__main__":
    sample_plan = get_water_fertilizer_plan("Rice", soil_N=30, soil_P=20, soil_K=25)
    print(sample_plan)
