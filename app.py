# app.py — AgriIntel (modern UI + Report Generator page, minimal-formal PDF)
import streamlit as st
import json
import io
from datetime import datetime

# Try import reportlab, handle if missing
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# Your existing modules (must exist in project)
from predictor import predict_crop
from water_fertilizer_plan import get_water_fertilizer_plan
from crop_companion import get_companion_crops
from crop_rotation_planner import suggest_next_crop
from indian_states_cities import indian_states_cities

st.set_page_config(page_title="AgriIntel", page_icon="🌾", layout="wide")

# Small CSS for clean cards/header
st.markdown(
    """
    <style>
    .section-title { font-size:22px; font-weight:700; color:lime; margin-bottom:6px;}
    .card { background: #fbfffb; border-radius:1px; padding:1px; box-shadow: 0 1px 6px rgba(0,0,0,0.06); }
    .muted { color: white; font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True, 
)

# Sidebar: navigation only (includes Report Generator)
with st.sidebar:
    st.title("AgriIntel")
    st.caption("Smart Crop Recommendation & ROI")
    page = st.radio(
        "Navigate",
        ("Recommendation", "Water & Fertilizer", "Rotation & Companion", "ROI", "Report Generator")
    )
    st.markdown("---")
    if not REPORTLAB_AVAILABLE:
        st.warning("PDF generation requires 'reportlab'. Install: pip install reportlab")

# Helper - area conversion
def convert_to_hectare(area, unit):
    mapping = {
        "Acre": 0.4047, "Guntha": 0.0101, "Bigha (Punjab)": 0.25,
        "Bigha (UP)": 0.25, "Bigha (West Bengal)": 0.13, "Bigha (Assam)": 0.33,
        "Vigha (Gujarat)": 0.16, "Kanal": 0.0506, "Marla": 0.0025,
        "Cent": 0.0040, "Hectare": 1.0
    }
    if unit not in mapping:
        raise ValueError("Invalid unit")
    return area * mapping[unit]

# -----------------------
# Recommendation Page
# -----------------------
if page == "Recommendation":
    st.markdown('<div class="section-title">🌱 Crop Recommendation</div> ', unsafe_allow_html=True)
    st.markdown('<div class="muted">Enter soil parameters and select location to get crop recommendation.</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        soil_list = ["Loamy", "Clay", "Sandy", "Black", "Red", "Alluvial", "Laterite"]
        col1, col2 = st.columns([1,1])
        with col1:
            N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50, key="rec_N")
            P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50, key="rec_P")
            K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=50, key="rec_K")
            ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1, key="rec_ph")
            soil_type = st.selectbox("Soil Type", soil_list, key="rec_soil")
        with col2:
            st.markdown("**Location for weather**")
            state = st.selectbox("State", list(indian_states_cities.keys()), key="rec_state")
            city = st.selectbox("City", indian_states_cities[state], key="rec_city")
            st.markdown("---")
            if st.button("🌤️ Get Recommended Crop", key="rec_button"):
                try:
                    recommended_crop = predict_crop(N, P, K, ph, soil_type, city)
                    st.session_state["recommended_crop"] = recommended_crop
                    st.success(f"✅ Recommended Crop: **{recommended_crop}**")
                    st.markdown(f"**Inputs:** Soil: {soil_type} | N:{N} P:{P} K:{K} | pH:{ph}")
                    st.markdown(f"**Location:** {city}, {state}")
                except Exception as e:
                    st.error(f"Prediction error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# Water & Fertilizer Page
# -----------------------
elif page == "Water & Fertilizer":
    st.markdown('<div class="section-title">💧 Water & Fertilizer Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">Select crop and soil test values to get irrigation & NPK plan.</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # choose crop (default to recommended if available)
        crop_list = ["Apple","Arecanut","Bajra","Barley","Banana", "Beans", "Beets", "Borage", "Basil", "Blackgram",
                     "Cashewnut", "Cabbage","Carrot","Cardamom","Castor Seed","Celery","Chickpea", "Coffee", "Coconut",
                     "Coriander" , "Corn", "Cotton","Cowpea","Cucumber","Dill","Dry Chillies", "Garlic","Ginger","Groundnut",
                     "Grapes","Guar seed","Horsegram", "Jowar","Jute","Kidneybeans","Khesari","Linseed", "Leek", "Lettuce",
                     "Lentil", "Mango", "Maize","Masoor", "Melon","Mesta","Mungbean", "Muskmelon","Mothbeans","Mustard",
                     "Niger seed", "Onion", "Orange", "Papaya","Pepper", "Pigeonpeas", "Potato", "Pumpkin", "Pomegranate",
                     "Radish","Ragi", "Rice", "Safflower","Sesamum","Soyabean","Sugarcane","Sunflower","Squash", "Spinach",
                     "Strawberry","Sweet Potato","Tapioca","Tobacco", "Tomato","Tur", "Turnip","Turmeric","Urad", "Watermelon","Wheat"]
        default_crop = st.session_state.get("recommended_crop", None)
        chosen_crop = st.selectbox("Select Crop (for plan)", options=crop_list, index=crop_list.index(default_crop) if default_crop in crop_list else 0, key="wf_crop")
        col1, col2 = st.columns(2)
        with col1:
            soil_N = st.number_input("Soil Nitrogen (N)", min_value=0.0, max_value=500.0, value=50.0, step=0.1, key="wf_N")
            soil_P = st.number_input("Soil Phosphorus (P)", min_value=0.0, max_value=500.0, value=50.0, step=0.1, key="wf_P")
        with col2:
            soil_K = st.number_input("Soil Potassium (K)", min_value=0.0, max_value=500.0, value=50.0, step=0.1, key="wf_K")
            soil_ph = st.number_input("Soil pH (optional)", min_value=0.0, max_value=14.0, value=6.5, step=0.1, key="wf_ph")
        if st.button("🔍 Generate Plan", key="wf_btn"):
            try:
                plan = get_water_fertilizer_plan(chosen_crop, soil_N=soil_N, soil_P=soil_P, soil_K=soil_K, ph=soil_ph)
                st.session_state["water_plan"] = plan
                if "error" in plan:
                    st.error(plan["error"])
                else:
                    left, right = st.columns(2)
                    with left:
                        st.subheader("Irrigation Recommendation")
                        st.info(plan.get("irrigation", "N/A"))
                        st.subheader("Notes")
                        st.write(plan.get("notes", "No specific notes."))
                    with right:
                        st.subheader("Recommended NPK (kg/ha)")
                        rec = plan.get("recommended_NPK", {})
                        st.write(f"N: {rec.get('N','-')}, P: {rec.get('P','-')}, K: {rec.get('K','-')}")
                        st.subheader("NPK Gaps (kg/ha)")
                        gaps = plan.get("nutrient_gaps", {})
                        st.write(f"N: {round(gaps.get('N',0),2)}, P: {round(gaps.get('P',0),2)}, K: {round(gaps.get('K',0),2)}")
            except Exception as e:
                st.error(f"Planner error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# Rotation & Companion Page
# -----------------------
elif page == "Rotation & Companion":
    st.markdown('<div class="section-title">🔄 Crop Rotation & 🌿 Companion Planner</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        crop_options = ["Apple","Arecanut","Bajra","Barley","Banana", "Beans", "Beets", "Borage", "Basil", "Blackgram",
                        "Cashewnut", "Cabbage","Carrot","Cardamom","Castor Seed","Celery", "Chickpea", "Coffee", "Coconut",
                        "Coriander" , "Corn", "Cotton","Cowpea","Cucumber","Dill","Dry Chillies", "Garlic","Ginger","Groundnut",
                        "Grapes","Guar seed","Horsegram", "Jowar","Jute","Kidneybeans","Khesari","Linseed", "Leek", "Lettuce",
                        "Lentil", "Mango", "Maize","Masoor", "Melon","Mesta","Mungbean", "Muskmelon","Mothbeans","Mustard",
                        "Niger seed", "Onion", "Orange", "Papaya","Pepper", "Pigeonpeas", "Potato", "Pumpkin", "Pomegranate",
                        "Radish","Ragi", "Rice", "Safflower","Sesamum","Soyabean","Sugarcane","Sunflower","Squash", "Spinach",
                        "Strawberry","Sweet Potato","Tapioca","Tobacco", "Tomato","Tur", "Turnip","Turmeric","Urad", "Watermelon","Wheat"]
        curr_crop = st.selectbox("Select Current Crop (for rotation)", crop_options, key="rot_curr")
        if st.button("🌾 Suggest Next Crops (Rotation)", key="rot_btn"):
            try:
                rotation_suggestions = suggest_next_crop(curr_crop)
                st.session_state["rotation"] = rotation_suggestions
                if "error" in rotation_suggestions:
                    st.error(rotation_suggestions["error"])
                else:
                    st.success(f"Suggested next crops after **{curr_crop}**:")
                    st.write(", ".join(rotation_suggestions.get("next", [])))
                    st.subheader("Notes")
                    st.info(rotation_suggestions.get("note", "No notes available."))
            except Exception as e:
                st.error(f"Rotation error: {e}")

        st.markdown("---")
        companion_crop = st.selectbox("Select Crop (for companions)", crop_options, key="comp_crop")
        if st.button("👩‍🌾 Get Companion Crops", key="comp_btn"):
            try:
                companions = get_companion_crops(companion_crop)
                st.session_state["companions"] = companions
                if "error" in companions:
                    st.error(companions["error"])
                else:
                    st.success(f"Companion crops for **{companion_crop}**:")
                    st.write(", ".join(companions.get("companions", [])))
                    st.markdown("Notes")
                    st.info(companions.get("notes", "No notes available."))
            except Exception as e:
                st.error(f"Companion error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# ROI Page
# -----------------------
elif page == "ROI":
    st.markdown('<div class="section-title">💰 ROI Calculator</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # load yields JSON
        try:
            with open("datasets/statewise_avg_yield.json", "r") as f:
                yield_data = json.load(f)
        except Exception as e:
            st.error(f"Could not load yield data: {e}")
            yield_data = {}

        col1, col2 = st.columns(2)
        with col1:
            Area = st.number_input("Enter Farm Size", value=1.0, min_value=0.0, step=0.1, key="roi_area")
            Measurement_list = ["Acre","Guntha","Bigha (Punjab)","Bigha (UP)","Bigha (West Bengal)","Bigha (Assam)",
                                "Vigha (Gujarat)","Kanal","Marla","Cent","Hectare"]
            Measurement_unit = st.selectbox("Measurement Unit", Measurement_list, key="roi_unit")
        with col2:
            roi_state = st.selectbox("Select State (for yield)", list(yield_data.keys()), key="roi_state")
            roi_crop = st.selectbox("Select Crop (state-specific)", list(yield_data[roi_state].keys()), key="roi_crop")

        farm_size = convert_to_hectare(Area, Measurement_unit)
        avg_yield = yield_data[roi_state][roi_crop]
        if roi_crop.lower() == "coconut":
            st.info("Coconut yield = nuts per hectare")
            total_yield_units = farm_size * avg_yield
            st.write(f"Estimated total coconut count: **{total_yield_units:.0f} nuts**")
            market_price_unit = st.number_input(f"Market price per coconut (₹)", value=1.0, key="roi_price_unit")
            revenue = market_price_unit * total_yield_units
            total_yield_kg = None
        else:
            total_yield_kg = farm_size * avg_yield * 1000
            st.write(f"Estimated total yield: **{total_yield_kg:.2f} kg**")
            market_price_per_kg = st.number_input(f"Market price per kg (₹) for {roi_crop}", value=10.0, key="roi_price_kg")
            revenue = market_price_per_kg * total_yield_kg

        input_cost = st.number_input("Total input cost (₹)", value=0.0, key="roi_input")
        irrigation_cost = st.number_input("Total irrigation cost (₹)", value=0.0, key="roi_irrig")
        labor_cost = st.number_input("Total labor cost (₹)", value=0.0, key="roi_labor")
        total_cost = input_cost + irrigation_cost + labor_cost
        profit = revenue - total_cost
        roi_percent = (profit / total_cost * 100) if total_cost > 0 else None

        st.session_state["roi"] = {
            "farm_size": farm_size,
            "crop": roi_crop,
            "state": roi_state,
            "total_yield_kg": total_yield_kg,
            "revenue": revenue,
            "total_cost": total_cost,
            "profit": profit,
            "market_price": market_price_per_kg if total_yield_kg is not None else market_price_unit
        }

        m1, m2, m3 = st.columns(3)
        m1.metric("Estimated Revenue", f"₹ {revenue:,.2f}")
        m2.metric("Total Cost", f"₹ {total_cost:,.2f}")
        if roi_percent is not None:
            m3.metric("Profit / ROI%", f"₹ {profit:,.2f} / {roi_percent:.2f}%")
        else:
            m3.metric("Profit", f"₹ {profit:,.2f}")

        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# Report Generator Page
# -----------------------
elif page == "Report Generator":
    st.markdown('<div class="section-title">📄 Report Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">This page collects the latest session results and generates a single minimal-formal PDF report.</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.write("The report will include: Crop Recommendation, Water & Fertilizer Plan, Companion & Rotation suggestions, and ROI summary.")
        if not REPORTLAB_AVAILABLE:
            st.warning("reportlab not installed. Run: pip install reportlab to enable PDF creation.")
        generate = st.button("🧾 Generate PDF Report", key="gen_report")

        if generate and REPORTLAB_AVAILABLE:
            # Collect data from session_state
            rec = st.session_state.get("recommended_crop", "Not calculated")
            water = st.session_state.get("water_plan", {})
            companions = st.session_state.get("companions", {})
            rotation = st.session_state.get("rotation", {})
            roi = st.session_state.get("roi", {})

            # Create PDF in-memory
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            normal = styles["Normal"]
            heading = styles["Heading2"]
            elements = []

            elements.append(Paragraph("AgriIntel — Comprehensive Report", styles['Title']))
            elements.append(Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), normal))
            elements.append(Spacer(1, 12))

            # Crop recommendation
            elements.append(Paragraph("1. Crop Recommendation", heading))
            elements.append(Paragraph(f"Recommended crop: {rec}", normal))
            elements.append(Spacer(1, 8))

            # Water & Fertilizer
            elements.append(Paragraph("2. Water & Fertilizer Plan", heading))
            if water:
                if "error" in water:
                    elements.append(Paragraph(f"Planner Error: {water.get('error')}", normal))
                else:
                    elements.append(Paragraph(f"Irrigation: {water.get('irrigation', 'N/A')}", normal))
                    gaps = water.get("nutrient_gaps", {})
                    recnpk = water.get("recommended_NPK", {})
                    elements.append(Paragraph(f"Recommended NPK (kg/ha): N:{recnpk.get('N','-')}, P:{recnpk.get('P','-')}, K:{recnpk.get('K','-')}", normal))
                    elements.append(Paragraph(f"NPK Gaps (kg/ha): N:{round(gaps.get('N',0),2)}, P:{round(gaps.get('P',0),2)}, K:{round(gaps.get('K',0),2)}", normal))
                    elements.append(Paragraph(f"Notes: {water.get('notes','')}", normal))
            else:
                elements.append(Paragraph("No water & fertilizer plan available in this session.", normal))
            elements.append(Spacer(1, 8))

            # Companion
            elements.append(Paragraph("3. Companion Crop Planner", heading))
            if companions:
                if "error" in companions:
                    elements.append(Paragraph(f"Companion Error: {companions.get('error')}", normal))
                else:
                    elements.append(Paragraph(f"Companion Crops: {', '.join(companions.get('companions', []))}", normal))
                    elements.append(Paragraph(f"Notes: {companions.get('notes','')}", normal))
            else:
                elements.append(Paragraph("No companion data available in this session.", normal))
            elements.append(Spacer(1, 8))

            # Rotation
            elements.append(Paragraph("4. Crop Rotation Planner", heading))
            if rotation:
                if "error" in rotation:
                    elements.append(Paragraph(f"Rotation Error: {rotation.get('error')}", normal))
                else:
                    elements.append(Paragraph(f"Next Crops: {', '.join(rotation.get('next', []))}", normal))
                    elements.append(Paragraph(f"Notes: {rotation.get('note','')}", normal))
            else:
                elements.append(Paragraph("No rotation data available in this session.", normal))
            elements.append(Spacer(1, 8))

            # ROI
            elements.append(Paragraph("5. ROI Summary", heading))
            if roi:
                farm_size = roi.get("farm_size", 0)
                total_yield_kg = roi.get("total_yield_kg", None)
                revenue = roi.get("revenue", 0)
                total_cost = roi.get("total_cost", roi.get("total_cost", roi.get("total_cost", 0)))
                profit = roi.get("profit", 0)

                data = [
                    ["Farm Size (ha)", "Yield (kg)", "Revenue (₹)", "Total Cost (₹)", "Profit (₹)"],
                    [f"{farm_size:.4f}", f"{total_yield_kg:.2f}" if total_yield_kg else "-", f"{revenue:.2f}", f"{total_cost:.2f}", f"{profit:.2f}"]
                ]
                table = Table(data, hAlign='LEFT')
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dfeadf')),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                    ('ALIGN',(2,0),(4,1),'RIGHT')
                ]))
                elements.append(table)
            else:
                elements.append(Paragraph("No ROI data available in this session.", normal))

            elements.append(Spacer(1, 12))
            doc.build(elements)
            buffer.seek(0)

            # Provide download
            filename = f"AgriIntel_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            st.download_button("⬇️ Download PDF Report", data=buffer, file_name=filename, mime="application/pdf")
        elif generate and not REPORTLAB_AVAILABLE:
            st.error("reportlab is not installed. Install it with: pip install reportlab")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer (common)
st.markdown("---")
st.markdown("<div style='text-align:center; color:#6b6b6b;'>Made with 🌾 by AgriIntel © Uttkarsh Khanke . All Rights Reserved</div>", unsafe_allow_html=True)
