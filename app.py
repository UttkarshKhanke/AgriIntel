# app.py
import streamlit as st
from predictor import predict_crop
from water_fertilizer_planner import get_water_fertilizer_plan

st.set_page_config(page_title="AgriIntel", page_icon="🌾")
st.title("🌾 AgriIntel: Crop Recommendation & Water/Fertilizer Planner")

st.markdown("### Enter Soil Parameters:")

# Soil inputs
N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50)
P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50)
K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=50)
ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1)

# City input for weather
city = st.text_input("Enter City for Weather Data")

st.markdown("### Get Recommended Crop based on Soil & Weather")

if st.button("🌱 Get Recommended Crop"):
    if city.strip() == "":
        st.warning("Please enter a city name to fetch weather data.")
    else:
        recommended_crop = predict_crop(N, P, K, ph, city)
        st.success(f"✅ Recommended Crop: **{recommended_crop}**")

# Divider
st.markdown("---")
st.markdown("### Get Water & Fertilizer Plan for a Selected Crop")

# Crop selection
crop_list = ["Rice", "Wheat", "Maize", "Chickpea", "Mungbean", "Banana", "Mango",
             "Grapes", "Cotton", "Coffee", "Tomato", "Potato"]  # Extend as needed
selected_crop = st.selectbox("Select Crop", crop_list)

if st.button("💧 Get Water & Fertilizer Plan"):
    plan = get_water_fertilizer_plan(selected_crop, soil_N=N, soil_P=P, soil_K=K, ph=ph)

    if "error" in plan:
        st.error(plan["error"])
    else:
        st.subheader("💧 Recommended Irrigation Plan")
        st.write(plan["irrigation"])

        st.subheader("🧪 Recommended Fertilizer Plan (NPK gaps)")
        st.write(f"N: {plan['nutrient_gaps']['N']} kg/ha, "
                 f"P: {plan['nutrient_gaps']['P']} kg/ha, "
                 f"K: {plan['nutrient_gaps']['K']} kg/ha")

        st.subheader("📌 Notes / Recommendations")
        st.write(plan["notes"])
