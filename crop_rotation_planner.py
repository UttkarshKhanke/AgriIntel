import pandas as pd

# Expanded crop rotation rules (simplified + realistic suggestions)
rotation_rules = {
    "Rice": ["Wheat", "Maize", "Lentil", "Mustard"],
    "Wheat": ["Rice", "Maize", "Pigeonpeas", "Soybean"],
    "Maize": ["Beans", "Cabbage", "Peas", "Potato"],
    "Chickpea": ["Maize", "Rice", "Millet", "Cotton"],
    "Kidneybeans": ["Maize", "Tomato", "Cabbage", "Carrot"],
    "Pigeonpeas": ["Maize", "Wheat", "Mustard", "Sesame"],
    "Mothbeans": ["Wheat", "Barley", "Mustard"],
    "Mungbean": ["Maize", "Rice", "Potato"],
    "Blackgram": ["Rice", "Maize", "Sorghum"],
    "Lentil": ["Rice", "Maize", "Mustard"],
    "Banana": ["Legumes", "Maize", "Sweet Potato"],
    "Mango": ["Legumes", "Vegetables"],
    "Grapes": ["Legumes", "Garlic", "Onion"],
    "Watermelon": ["Maize", "Groundnut", "Onion"],
    "Muskmelon": ["Maize", "Wheat", "Potato"],
    "Apple": ["Legumes", "Barley", "Mustard"],
    "Orange": ["Legumes", "Onion", "Garlic"],
    "Papaya": ["Legumes", "Maize"],
    "Coconut": ["Pineapple", "Banana", "Legumes"],
    "Cotton": ["Wheat", "Mustard", "Barley"],
    "Jute": ["Potato", "Mustard", "Wheat"],
    "Coffee": ["Banana", "Beans", "Legumes"],
    "Tomato": ["Onion", "Garlic", "Spinach", "Cabbage"],
    "Basil": ["Tomato", "Peppers", "Lettuce"],
    "Carrot": ["Lettuce", "Onion", "Beans"],
    "Onion": ["Tomato", "Cabbage", "Spinach"],
    "Corn": ["Soybean", "Beans", "Peas"],
    "Beans": ["Corn", "Cabbage", "Carrot"],
    "Squash": ["Corn", "Beans", "Radish"],
    "Leek": ["Carrot", "Lettuce", "Spinach"],
    "Lettuce": ["Carrot", "Onion", "Beets"],
    "Cabbage": ["Potato", "Beans", "Carrot"],
    "Dill": ["Cabbage", "Lettuce", "Cucumber"],
    "Celery": ["Onion", "Leek", "Beans"],
    "Potato": ["Cabbage", "Beans", "Spinach"],
    "Spinach": ["Onion", "Carrot", "Beans"],
    "Radish": ["Lettuce", "Spinach", "Peas"],
    "Strawberry": ["Lettuce", "Spinach", "Beans"],
    "Turnip": ["Spinach", "Peas", "Barley"],
    "Cucumber": ["Beans", "Corn", "Radish"],
    "Pumpkin": ["Corn", "Beans", "Squash"],
    "Beets": ["Lettuce", "Onion", "Cabbage"],
    "Garlic": ["Tomato", "Cabbage", "Lettuce"],
    "Pepper": ["Basil", "Onion", "Spinach"],
    "Borage": ["Tomato", "Strawberry", "Squash"]
}

def suggest_next_crop(prev_crop: str, curr_crop: str):
    """
    Suggests next crops based on crop rotation rules.
    """
    if curr_crop not in rotation_rules:
        return {"error": f"No rotation data available for crop '{curr_crop}'"}

    # Simple rule: suggest based on current crop
    return rotation_rules[curr_crop]

# Quick test
if __name__ == "__main__":
    print(suggest_next_crop("Wheat", "Rice"))
