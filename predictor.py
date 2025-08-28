import joblib
import numpy as np
from weather_api import get_weather

# Load model
model = joblib.load("models/crop_recommendation_model.pkl")

def predict_crop(N, P, K, ph, city):
    try:
        temperature, humidity, rainfall = get_weather(city)
    except Exception as e:
        return f"⚠️ Weather API Error: {e}"

    # Prepare input
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    
    # Predict
    prediction = model.predict(features)
    return prediction[0]
