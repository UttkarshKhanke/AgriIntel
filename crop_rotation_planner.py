import pandas as pd

# ======================
# 🌱 Realistic Crop Rotation Rules (Only from your list)
# ======================
rotation_rules = {
    "Apple": {
        "next": ["Beans", "Clover", "Mustard"],
        "note": "Legumes like beans fix nitrogen; mustard reduces orchard pests."
    },
    "Arecanut": {
        "next": ["Banana", "Pepper", "Ginger"],
        "note": "Shade-tolerant intercrops maintain soil moisture and fertility."
    },
    "Bajra": {
        "next": ["Chickpea", "Mustard", "Cowpea"],
        "note": "Legumes replenish nitrogen; mustard suppresses soil pathogens."
    },
    "Barley": {
        "next": ["Chickpea", "Lentil", "Linseed"],
        "note": "Legumes and oilseeds improve soil balance after barley."
    },
    "Banana": {
        "next": ["Cowpea", "Ginger", "Groundnut"],
        "note": "Legumes and ginger improve organic matter post banana."
    },
    "Beans": {
        "next": ["Maize", "Wheat", "Tomato"],
        "note": "Cereals and solanaceous crops utilize nitrogen fixed by beans."
    },
    "Beets": {
        "next": ["Onion", "Lettuce", "Carrot"],
        "note": "Rotating with root and leafy crops maintains nutrient diversity."
    },
    "Borage": {
        "next": ["Cabbage", "Carrot", "Lettuce"],
        "note": "Leafy crops and roots grow well after borage enriches soil."
    },
    "Basil": {
        "next": ["Tomato", "Carrot", "Cabbage"],
        "note": "Tomato benefits from basil rotation; root crops restore nutrients."
    },
    "Blackgram": {
        "next": ["Rice", "Wheat", "Maize"],
        "note": "Excellent nitrogen fixer; followed by cereals for balance."
    },
    "Cashewnut": {
        "next": ["Coconut", "Pepper", "Ginger"],
        "note": "Intercropping with spices and coconut maintains fertility."
    },
    "Cabbage": {
        "next": ["Carrot", "Onion", "Tomato"],
        "note": "Avoid continuous brassicas; rotate with root and fruit crops."
    },
    "Carrot": {
        "next": ["Onion", "Cabbage", "Spinach"],
        "note": "Rotating root, leafy, and bulb crops prevents nutrient depletion."
    },
    "Cardamom": {
        "next": ["Ginger", "Turmeric", "Pepper"],
        "note": "Spice crops thrive under similar shade and moisture levels."
    },
    "Castor Seed": {
        "next": ["Maize", "Chickpea", "Lentil"],
        "note": "Legumes improve nitrogen; maize uses residual oilseed nutrients."
    },
    "Celery": {
        "next": ["Carrot", "Onion", "Spinach"],
        "note": "Root and leafy crops maintain soil health after celery."
    },
    "Chickpea": {
        "next": ["Maize", "Wheat", "Mustard"],
        "note": "Cereals and oilseeds follow legumes well for balanced rotation."
    },
    "Coffee": {
        "next": ["Blackgram", "Ginger", "Pepper"],
        "note": "Nitrogen-fixing and shade crops thrive under coffee canopy."
    },
    "Coconut": {
        "next": ["Banana", "Pepper", "Ginger"],
        "note": "Shade-tolerant crops increase biodiversity under palms."
    },
    "Coriander": {
        "next": ["Cabbage", "Carrot", "Lettuce"],
        "note": "Leafy and root crops improve soil texture after coriander."
    },
    "Corn": {
        "next": ["Soyabean", "Groundnut", "Mustard"],
        "note": "Legumes and oilseeds replenish nutrients after cereals."
    },
    "Cotton": {
        "next": ["Lentil", "Chickpea", "Sunflower"],
        "note": "Legumes improve nitrogen; sunflower restores deep nutrients."
    },
    "Cowpea": {
        "next": ["Maize", "Rice", "Wheat"],
        "note": "Cereals utilize nitrogen fixed by cowpea."
    },
    "Cucumber": {
        "next": ["Beans", "Onion", "Spinach"],
        "note": "Leafy and legumes improve soil and pest balance after cucurbits."
    },
    "Dill": {
        "next": ["Carrot", "Beets", "Lettuce"],
        "note": "Root and leafy crops follow well to restore soil fertility."
    },
    "Dry Chillies": {
        "next": ["Onion", "Maize", "Cabbage"],
        "note": "Rotating with non-solanaceous crops avoids pest carryover."
    },
    "Garlic": {
        "next": ["Tomato", "Cabbage", "Spinach"],
        "note": "Leafy and fruit crops benefit from garlic’s pest-repelling effect."
    },
    "Ginger": {
        "next": ["Maize", "Cowpea", "Turmeric"],
        "note": "Legumes and cereals help replenish organic matter."
    },
    "Groundnut": {
        "next": ["Rice", "Wheat", "Maize"],
        "note": "Cereals benefit from nitrogen fixed by groundnut roots."
    },
    "Grapes": {
        "next": ["Garlic", "Cowpea", "Coriander"],
        "note": "Garlic repels pests; legumes and herbs enhance vineyard soil."
    },
    "Guar seed": {
        "next": ["Maize", "Wheat", "Mustard"],
        "note": "Cereals utilize nitrogen fixed by guar."
    },
    "Horsegram": {
        "next": ["Rice", "Maize", "Wheat"],
        "note": "Legume rotation improves nitrogen and breaks pest cycles."
    },
    "Jowar": {
        "next": ["Lentil", "Chickpea", "Mustard"],
        "note": "Legumes and oilseeds restore fertility after sorghum."
    },
    "Jute": {
        "next": ["Rice", "Maize", "Lentil"],
        "note": "Legumes and cereals balance nutrient extraction of jute."
    },
    "Kidneybeans": {
        "next": ["Maize", "Wheat", "Mustard"],
        "note": "Cereals and oilseeds utilize residual nitrogen effectively."
    },
    "Khesari": {
        "next": ["Maize", "Rice", "Mustard"],
        "note": "Good nitrogen fixer; followed by cereals and oilseeds."
    },
    "Linseed": {
        "next": ["Maize", "Lentil", "Chickpea"],
        "note": "Cereals and legumes balance soil nutrients after oilseed."
    },
    "Leek": {
        "next": ["Carrot", "Cabbage", "Spinach"],
        "note": "Root and leafy crops restore nutrients after leeks."
    },
    "Lettuce": {
        "next": ["Onion", "Carrot", "Beans"],
        "note": "Rotating leafy, bulb, and legume crops keeps soil balanced."
    },
    "Lentil": {
        "next": ["Maize", "Wheat", "Mustard"],
        "note": "Legume-cereal-oilseed sequence sustains soil fertility."
    },
    "Mango": {
        "next": ["Cowpea", "Ginger", "Turmeric"],
        "note": "Legumes and spices improve orchard soil biodiversity."
    },
    "Maize": {
        "next": ["Chickpea", "Soyabean", "Mustard"],
        "note": "Legume-oilseed rotation optimizes nitrogen and pest control."
    },
    "Masoor": {
        "next": ["Maize", "Wheat", "Mustard"],
        "note": "Cereal and oilseed crops utilize legume-fixed nitrogen."
    },
    "Melon": {
        "next": ["Cowpea", "Cabbage", "Onion"],
        "note": "Non-cucurbits reduce pest and disease incidence."
    },
    "Mesta": {
        "next": ["Rice", "Maize", "Lentil"],
        "note": "Legumes improve soil fertility after fiber crops."
    },
    "Mungbean": {
        "next": ["Rice", "Maize", "Wheat"],
        "note": "Ideal pre-cereal legume to restore nitrogen."
    },
    "Muskmelon": {
        "next": ["Cowpea", "Onion", "Tomato"],
        "note": "Leafy and fruit crops diversify nutrients post melon."
    },
    "Mothbeans": {
        "next": ["Wheat", "Maize", "Mustard"],
        "note": "Legume rotation benefits cereals and oilseeds."
    },
    "Mustard": {
        "next": ["Rice", "Maize", "Wheat"],
        "note": "Oilseed-cereal rotation balances nitrogen and pest cycles."
    },
    "Niger seed": {
        "next": ["Rice", "Lentil", "Chickpea"],
        "note": "Legume sequence replenishes fertility after oilseed."
    },
    "Onion": {
        "next": ["Cabbage", "Carrot", "Tomato"],
        "note": "Avoid same family; root and fruit crops are best after onion."
    },
    "Orange": {
        "next": ["Cowpea", "Coriander", "Ginger"],
        "note": "Legumes and spices enhance orchard soil fertility."
    },
    "Papaya": {
        "next": ["Cowpea", "Groundnut", "Soyabean"],
        "note": "Legumes restore nitrogen after papaya cultivation."
    },
    "Pepper": {
        "next": ["Ginger", "Turmeric", "Banana"],
        "note": "Spices and banana thrive in similar shaded conditions."
    },
    "Pigeonpeas": {
        "next": ["Rice", "Wheat", "Maize"],
        "note": "Legume-cereal rotation enhances nitrogen use efficiency."
    },
    "Potato": {
        "next": ["Maize", "Soyabean", "Mustard"],
        "note": "Follow tubers with cereals or legumes to rebalance soil."
    },
    "Pumpkin": {
        "next": ["Corn", "Cowpea", "Onion"],
        "note": "Cereals and legumes improve soil after cucurbits."
    },
    "Pomegranate": {
        "next": ["Cowpea", "Coriander", "Ginger"],
        "note": "Short-term crops maintain soil health between fruit cycles."
    },
    "Radish": {
        "next": ["Onion", "Lettuce", "Beans"],
        "note": "Legumes and leafy crops maintain nutrient diversity."
    },
    "Ragi": {
        "next": ["Horsegram", "Cowpea", "Pigeonpeas"],
        "note": "Legumes improve soil nitrogen after millet harvest."
    },
    "Rice": {
        "next": ["Wheat", "Maize", "Lentil"],
        "note": "Cereal-legume rotation sustains soil fertility and yield."
    },
    "Safflower": {
        "next": ["Lentil", "Chickpea", "Wheat"],
        "note": "Legume-cereal rotation prevents nutrient exhaustion."
    },
    "Sesamum": {
        "next": ["Rice", "Maize", "Cowpea"],
        "note": "Cereal-legume rotation restores nutrient balance."
    },
    "Soyabean": {
        "next": ["Wheat", "Maize", "Mustard"],
        "note": "Cereal-oilseed cycle utilizes residual nitrogen."
    },
    "Sugarcane": {
        "next": ["Lentil", "Wheat", "Maize"],
        "note": "Heavy feeder followed by legumes and cereals restores fertility."
    },
    "Sunflower": {
        "next": ["Chickpea", "Lentil", "Rice"],
        "note": "Legume-cereal rotation enhances organic matter."
    },
    "Squash": {
        "next": ["Cowpea", "Maize", "Spinach"],
        "note": "Legumes and leafy crops restore soil nutrients."
    },
    "Spinach": {
        "next": ["Carrot", "Onion", "Tomato"],
        "note": "Root and fruit crops prevent continuous nutrient use."
    },
    "Strawberry": {
        "next": ["Beans", "Clover", "Cowpea"],
        "note": "Legumes improve nitrogen and reduce soil-borne diseases."
    },
    "Sweet Potato": {
        "next": ["Maize", "Soyabean", "Cowpea"],
        "note": "Legume and cereal crops utilize leftover nutrients efficiently."
    },
    "Tapioca": {
        "next": ["Maize", "Cowpea", "Mustard"],
        "note": "Legume rotation maintains nitrogen after root crops."
    },
    "Tobacco": {
        "next": ["Maize", "Soyabean", "Cowpea"],
        "note": "Legumes and cereals restore nitrogen and prevent disease."
    },
    "Tomato": {
        "next": ["Cabbage", "Spinach", "Onion"],
        "note": "Alternate solanaceous crops with leafy and bulb crops."
    },
    "Tur": {
        "next": ["Rice", "Maize", "Wheat"],
        "note": "Legume-cereal sequence maintains soil fertility."
    },
    "Turnip": {
        "next": ["Carrot", "Onion", "Spinach"],
        "note": "Root-leafy rotation improves soil organic content."
    },
    "Turmeric": {
        "next": ["Maize", "Cowpea", "Ginger"],
        "note": "Legumes and cereals maintain soil fertility post spice crop."
    },
    "Urad": {
        "next": ["Rice", "Maize", "Wheat"],
        "note": "Legume-cereal sequence maintains soil nitrogen."
    },
    "Watermelon": {
        "next": ["Cowpea", "Maize", "Onion"],
        "note": "Rotating with legumes and cereals improves yield and pest control."
    },
    "Wheat": {
        "next": ["Rice", "Maize", "Soyabean"],
        "note": "Cereal-legume rotation sustains soil structure and fertility."
    }
}

# ======================
# 🌿 Suggestion Function
# ======================
def suggest_next_crop(curr_crop: str):
    """
    Suggests next crops and notes based on crop rotation rules.
    """
    if curr_crop not in rotation_rules:
        return {"error": f"No rotation data available for crop '{curr_crop}'"}

    data = rotation_rules[curr_crop]

    # If the data is a list, wrap it for consistent output
    if isinstance(data, list):
        return {
            "next": data,
            "note": "No specific note available for this crop rotation."
        }

    # Otherwise, it already has 'next' and 'note' keys
    return data

# ======================
# 🔬 Test
# ======================
if __name__ == "__main__":
    crop = "Maize"
    suggestion = suggest_next_crop(crop)
    print(f"Next Crop Options for {crop}: {suggestion['next']}")
    print(f"Notes: {suggestion['note']}")
