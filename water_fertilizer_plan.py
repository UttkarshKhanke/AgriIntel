import os
import pickle
import pandas as pd

# Paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "water_fertilizer_model.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "datasets", "crop_water_fertilizer_plan.csv")

# Load trained ML model and encoders
with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

model = data["model"]
crop_encoder = data["crop_encoder"]
irrigation_encoder = data["irrigation_encoder"]
notes_encoder = data["notes_encoder"]

# Load CSV knowledge base
crop_df = pd.read_csv(DATA_PATH)


def get_water_fertilizer_plan(crop_name: str, soil_N: int, soil_P: int, soil_K: int, ph: float = 6.5):
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

    # Compute nutrient gaps (rounded to 2 decimals)
    gap_N = round(max(0, recommended_N - soil_N), 2)
    gap_P = round(max(0, recommended_P - soil_P), 2)
    gap_K = round(max(0, recommended_K - soil_K), 2)

    # Encode crop name for model
    crop_encoded = crop_encoder.transform([crop_name])[0]

    # Predict irrigation type using model
    irrigation_pred_encoded = model.predict([[crop_encoded, soil_N, soil_P, soil_K, ph]])[0]
    irrigation_type = irrigation_encoder.inverse_transform([irrigation_pred_encoded])[0]

    # Create structured plan
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
    print("\n Recommended Fertilizer Plan:")
    print(f"Crop: {sample_plan['crop']}")
    print(f"Irrigation Type: {sample_plan['irrigation']}")
    print("NPK Gaps (kg/ha):", 
          f"N: {sample_plan['nutrient_gaps']['N']:.2f},",
          f"P: {sample_plan['nutrient_gaps']['P']:.2f},",
          f"K: {sample_plan['nutrient_gaps']['K']:.2f}")
    print(f"Notes: {sample_plan['notes']}")
