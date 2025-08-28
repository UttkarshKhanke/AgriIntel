import streamlit as st
from predictor import predict_crop

st.set_page_config(page_title="AgriIntel", page_icon="🌾")

st.title("🌾 AgriIntel: Crop Recommendation System")

st.markdown("### Enter Soil Parameters:")

N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50)
P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50)
K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=50)
ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
city = st.text_input("Enter City for Weather Data")

if st.button("🌱 Recommend Crop"):
    if city.strip() == "":
        st.warning("Please enter a city name to fetch weather data.")
    else:
        crop = predict_crop(N, P, K, ph, city)
        st.success(f"✅ Recommended Crop: **{crop}**")
