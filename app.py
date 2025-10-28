# app.py
import streamlit as st
from predictor import predict_crop
from water_fertilizer_planner import get_water_fertilizer_plan
from crop_companion import get_companion_crops
from crop_rotation_planner import suggest_next_crop
from indian_states_cities import indian_states_cities  

st.set_page_config(page_title="AgriIntel", page_icon="🌾")
st.title("🌾 AgriIntel: Crop Recommendation & Water/Fertilizer Planner")

soil_list = ["Loamy", "Clay", "Sandy", "Black", "Red", "Alluvial", "Laterite"]
st.markdown("### Enter Soil Parameters:")

# Soil inputs
N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50)
P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50)
K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=50)
ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
soil_type = st.selectbox("Select Soil", soil_list)

# City input for weather
st.markdown("### Select Location for Weather Data")

# State selection
state = st.selectbox("Select State", list(indian_states_cities.keys()))

# City selection (depends on state)
city = st.selectbox("Select City", indian_states_cities[state])

st.markdown("### Get Recommended Crop based on Soil & Weather")

if st.button("🌱 Get Recommended Crop"):
    if city.strip() == "":
        st.warning("Please enter a city name to fetch weather data.")
    else:
        recommended_crop = predict_crop(N, P, K, ph, soil_type,city)
        st.success(f"✅ Recommended Crop: **{recommended_crop}**")

# Divider
st.markdown("---")
st.markdown("### Get Water & Fertilizer Plan for a Selected Crop")

# Crop selection
crop_list = ["Apple","Arecanut",
            "Bajra","Barley","Banana", "Beans", "Beets", "Borage", "Basil", "Blackgram",
            "Cashewnut", "Cabbage","Carrot","Cardamom","Castor Seed","Celery",
            "Chickpea", "Coffee", "Coconut","Coriander" , "Corn", "Cotton","Cowpea","Cucumber",
            "Dill","Dry Chillies", "Garlic","Ginger","Groundnut",
            "Grapes","Guar seed","Horsegram", "Jowar","Jute","Kidneybeans","Khesari","Linseed", "Leek", "Lettuce",
            "Lentil", "Mango", "Maize","Masoor", "Melon","Mesta",
            "Mungbean", "Muskmelon","Mothbeans","Mustard","Niger seed", "Onion", "Orange", "Papaya",
            "Pepper", "Pigeonpeas", "Potato", "Pumpkin", "Pomegranate",
            "Radish","Ragi", "Rice", "Safflower","Sesamum","Soyabean","Sugarcane",
            "Sunflower","Squash", "Spinach", "Strawberry","Sweet Potato",
            "Tapioca","Tobacco", "Tomato","Tur", "Turnip","Turmeric","Urad", "Watermelon","Wheat"]  # Extend as needed
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

# Companion Crop Planner
st.subheader("🌱 Companion Crop Planner")

if st.button("👩‍🌾 Get Companion Crops"):
    if not selected_crop:
        st.warning("Please select a crop first.")
    else:
        companions = get_companion_crops(selected_crop)
        if "error" in companions:
            st.error(companions["error"])
        else:
            st.success(f"🌿 Companion crops for **{selected_crop}**:")
            st.write(", ".join(companions["companions"]))
            st.info(f"📝 Notes: {companions['notes']}")


# Crop Rotation Planner
st.subheader("🔄 Crop Rotation Planner")

# Crop options (same list as your dataset)
crop_options = ["Apple","Arecanut",
            "Bajra","Barley","Banana", "Beans", "Beets", "Borage", "Basil", "Blackgram",
            "Cashewnut", "Cabbage","Carrot","Cardamom","Castor Seed","Celery",
            "Chickpea", "Coffee", "Coconut","Coriander" , "Corn", "Cotton","Cowpea","Cucumber",
            "Dill","Dry Chillies", "Garlic","Ginger","Groundnut",
            "Grapes","Guar seed","Horsegram", "Jowar","Jute","Kidneybeans","Khesari","Linseed", "Leek", "Lettuce",
            "Lentil", "Mango", "Maize","Masoor", "Melon","Mesta",
            "Mungbean", "Muskmelon","Mothbeans","Mustard","Niger seed", "Onion", "Orange", "Papaya",
            "Pepper", "Pigeonpeas", "Potato", "Pumpkin", "Pomegranate",
            "Radish","Ragi", "Rice", "Safflower","Sesamum","Soyabean","Sugarcane",
            "Sunflower","Squash", "Spinach", "Strawberry","Sweet Potato",
            "Tapioca","Tobacco", "Tomato","Tur", "Turnip","Turmeric","Urad", "Watermelon","Wheat"] # Extend as needed

# Dropdowns for selecting crops
prev_crop = st.selectbox("🌱 Select Previous Crop", crop_options, key="prev_crop")
curr_crop = st.selectbox("🌾 Select Current Crop", crop_options, key="curr_crop")

if st.button("🌾 Suggest Next Crops"):
    if not prev_crop or not curr_crop:
        st.warning("Please select both previous and current crops.")
    else:
        rotation_suggestions = suggest_next_crop(prev_crop, curr_crop)

        if "error" in rotation_suggestions:
            st.error(rotation_suggestions["error"])
        else:
            st.success(f"🌱 Suggested next crops after **{curr_crop}**:")
            st.write(", ".join(rotation_suggestions))

