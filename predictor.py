import joblib
import numpy as np
from weather_api import get_weather

# Load saved objects
model_data = joblib.load("models/crop_recommendation_model.pkl")
model = model_data["model"]
scaler = model_data["scaler"]
label_encoder = model_data["label_encoder"]
soil_encoder = model_data["soil_encoder"]

def predict_crop(N, P, K, ph, soil_type, city):
    try:
        temperature, humidity, rainfall = get_weather(city)
    except Exception as e:
        return f"⚠️ Weather API Error: {e}"

    # Encode soil type
    if soil_type not in soil_encoder.classes_:
        return f"⚠️ Unknown soil type: '{soil_type}'. Please choose a valid one."

    soil_encoded = soil_encoder.transform([soil_type])[0]

    # Prepare features
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall, soil_encoded]])
    features_scaled = scaler.transform(features)

    # Predict
    prediction_encoded = model.predict(features_scaled)[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]
    return prediction_label
