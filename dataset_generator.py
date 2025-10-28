import pandas as pd
import random

#Define the soil types
soil_types = ["Loamy", "Clay", "Sandy", "Black", "Red", "Alluvial", "Laterite"]
# Define realistic crop-wise parameter ranges (approx. India conditions)
crop_conditions = {
    "Apple":        {"N": (40, 80), "P": (20, 50), "K": (30, 60), "temp": (8, 22), "hum": (40, 70), "ph": (5.5, 6.8), "rain": (600, 1200), "soil": ["Loamy", "Sandy"]},
    "Arecanut":     {"N": (80, 130), "P": (40, 70), "K": (80, 140), "temp": (23, 34), "hum": (75, 90), "ph": (5.0, 6.5), "rain": (1500, 3000), "soil": ["Laterite", "Clay"]},
    "Bajra":        {"N": (40, 80), "P": (20, 40), "K": (20, 50), "temp": (25, 38), "hum": (30, 60), "ph": (6.0, 7.5), "rain": (200, 600), "soil": ["Sandy", "Loamy","Red"]},
    "Barley":       {"N": (30, 70), "P": (20, 45), "K": (20, 50), "temp": (10, 24), "hum": (35, 65), "ph": (6.0, 7.5), "rain": (200, 600), "soil": ["Loamy", "Sandy","Clay","Alluvial"]},
    "Banana":       {"N": (100,160), "P": (40, 80), "K": (150,300), "temp": (22, 32), "hum": (70, 90), "ph": (5.0, 7.0), "rain": (1000, 2500), "soil": ["Alluvial", "Clay ","Loamy","Laterite"]},
    "Beans":        {"N": (20, 60), "P": (20, 40), "K": (20, 50), "temp": (15, 30), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (300, 800), "soil": ["Loamy", "Clay","Laterite"]},
    "Beets":        {"N": (50, 90), "P": (30, 55), "K": (40, 80), "temp": (8, 25), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (300, 700), "soil": ["Sandy", "Loamy"]},
    "Borage":       {"N": (30, 70), "P": (20, 40), "K": (20, 50), "temp": (12, 28), "hum": (45, 70), "ph": (6.0, 7.5), "rain": (300, 700), "soil": ["Loamy", "Sandy"]},
    "Basil":        {"N": (30, 70), "P": (15, 35), "K": (20, 50), "temp": (18, 30), "hum": (45, 75), "ph": (6.0, 7.5), "rain": (300, 800), "soil": ["Loamy", "Sandy"]},
    "Blackgram":    {"N": (5, 40),  "P": (15, 40), "K": (0, 30),  "temp": (22, 35), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Clay", "Loamy"]},
    "Cashewnut":    {"N": (60,120), "P": (30, 60), "K": (40, 90), "temp": (22, 34), "hum": (60, 80), "ph": (5.0, 6.8), "rain": (1000, 2500), "soil": ["Laterite", "Sandy"]},
    "Cabbage":      {"N": (50,100), "P": (30, 60), "K": (40, 80), "temp": (15, 25), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (500, 800), "soil": ["Loamy", "Clay"]},
    "Carrot":       {"N": (40, 90), "P": (30, 60), "K": (30, 60), "temp": (12, 25), "hum": (50, 75), "ph": (6.0, 6.8), "rain": (500, 800), "soil": ["Sandy", "Loamy"]},
    "Cardamom":     {"N": (70,120), "P": (30, 60), "K": (40, 80), "temp": (18, 28), "hum": (70, 90), "ph": (5.5, 6.5), "rain": (1500, 3000), "soil": ["Laterite", "Clay"]},
    "Castor Seed":  {"N": (50,100), "P": (30, 60), "K": (40, 80), "temp": (20, 35), "hum": (40, 70), "ph": (6.0, 7.5), "rain": (500, 900), "soil": ["Sandy", "Black","Red"]},
    "Celery":       {"N": (50,100), "P": (30, 50), "K": (40, 80), "temp": (12, 22), "hum": (60, 80), "ph": (6.0, 7.0), "rain": (500, 800), "soil": ["Loamy", "Clay"]},
    "Chickpea":     {"N": (10, 40), "P": (20, 50), "K": (10, 40), "temp": (20, 30), "hum": (40, 70), "ph": (6.0, 8.0), "rain": (400, 700), "soil": ["Sandy", "Black","Loamy"]},
    "Coffee":       {"N": (80,140), "P": (50, 90), "K": (80,120), "temp": (18, 28), "hum": (70, 90), "ph": (5.0, 6.5), "rain": (1500, 2500), "soil": ["Loamy", "Laterite"]},
    "Coconut":      {"N": (80,150), "P": (50, 90), "K": (80,140), "temp": (22, 34), "hum": (70, 90), "ph": (5.5, 7.0), "rain": (1000, 2500), "soil": ["Sandy", "Alluvial","Loamy","Laterite"]},
    "Coriander":    {"N": (30, 70), "P": (20, 45), "K": (30, 60), "temp": (20, 30), "hum": (50, 70), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Loamy", "Sandy"]},
    "Corn":         {"N": (60,120), "P": (40, 70), "K": (50,100), "temp": (20, 32), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (500, 1000), "soil": ["Loamy", "Alluvial"]},
    "Cotton":       {"N": (50,120), "P": (30, 70), "K": (40, 90), "temp": (25, 35), "hum": (50, 80), "ph": (6.0, 8.0), "rain": (600, 1200), "soil": ["Black", "Loamy","Clay"]},
    "Cowpea":       {"N": (20, 50), "P": (20, 40), "K": (20, 50), "temp": (20, 35), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Loamy", "Sandy","Clay","Black"]},
    "Cucumber":     {"N": (40, 80), "P": (30, 60), "K": (40, 80), "temp": (20, 30), "hum": (60, 80), "ph": (5.5, 7.0), "rain": (500, 1000), "soil": ["Sandy", "Loamy"]},
    "Dill":         {"N": (30, 70), "P": (20, 40), "K": (30, 60), "temp": (15, 30), "hum": (50, 70), "ph": (6.0, 7.5), "rain": (300, 800), "soil": ["Loamy", "Sandy "]},
    "Dry Chillies": {"N": (40, 90), "P": (20, 50), "K": (30, 60), "temp": (20, 32), "hum": (50, 70), "ph": (6.0, 7.5), "rain": (500, 1000), "soil": ["Sandy", "Black"]},
    "Garlic":       {"N": (50, 90), "P": (40, 60), "K": (30, 60), "temp": (12, 25), "hum": (60, 80), "ph": (6.0, 7.5), "rain": (400, 800), "soil": ["Sandy", "Loamy"]},
    "Ginger":       {"N": (60,120), "P": (40, 80), "K": (40, 90), "temp": (22, 30), "hum": (70, 90), "ph": (5.5, 6.8), "rain": (1500, 2500), "soil": ["Loamy", "Clay","Laterite"]},
    "Groundnut":    {"N": (20, 60), "P": (20, 50), "K": (20, 60), "temp": (25, 35), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (500, 1000), "soil": ["Sandy", "Loamy","Red"]},
    "Grapes":       {"N": (60,100), "P": (40, 70), "K": (50, 90), "temp": (15, 30), "hum": (60, 80), "ph": (6.0, 7.5), "rain": (500, 900), "soil": ["Sandy", "Loamy"]},
    "Guar seed":    {"N": (20, 50), "P": (15, 40), "K": (20, 50), "temp": (25, 35), "hum": (30, 60), "ph": (6.0, 7.5), "rain": (250, 600), "soil": ["Sandy", "Loamy"]},
    "Horsegram":    {"N": (10, 40), "P": (10, 40), "K": (10, 40), "temp": (20, 35), "hum": (40, 70), "ph": (6.0, 7.5), "rain": (300, 800), "soil": ["Loamy", "Sandy","Red"]},
    "Jowar":        {"N": (40, 80), "P": (20, 40), "K": (30, 60), "temp": (25, 38), "hum": (40, 70), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Loamy", "Black","Clay"]},
    "Jute":         {"N": (40, 90), "P": (30, 60), "K": (40, 90), "temp": (24, 34), "hum": (70, 90), "ph": (5.5, 7.0), "rain": (1200, 2500), "soil": ["Alluvial", "Clay"]},
    "Kidneybeans":  {"N": (20, 50), "P": (30, 60), "K": (20, 50), "temp": (18, 28), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (400, 800), "soil": ["Loamy", "Sandy"]},
    "Khesari":      {"N": (10, 40), "P": (10, 30), "K": (10, 40), "temp": (20, 30), "hum": (40, 70), "ph": (6.0, 8.0), "rain": (400, 800), "soil": ["Clay", "Loamy"]},
    "Linseed":      {"N": (20, 50), "P": (20, 50), "K": (20, 50), "temp": (15, 30), "hum": (50, 70), "ph": (6.0, 7.5), "rain": (400, 800), "soil": ["Loamy", "Clay","Black"]},
    "Leek":         {"N": (50, 90), "P": (30, 60), "K": (40, 80), "temp": (12, 25), "hum": (60, 80), "ph": (6.0, 7.0), "rain": (500, 800), "soil": ["Sandy", "Loamy"]},
    "Lettuce":      {"N": (50, 90), "P": (30, 50), "K": (40, 70), "temp": (12, 25), "hum": (60, 80), "ph": (6.0, 7.0), "rain": (400, 800), "soil": ["Sandy", "Loamy"]},
    "Lentil":       {"N": (10, 40), "P": (20, 50), "K": (10, 40), "temp": (15, 30), "hum": (40, 70), "ph": (6.0, 8.0), "rain": (400, 800), "soil": ["Loamy", "Clay","Alluvial"]},
    "Mango":        {"N": (50,100), "P": (30, 60), "K": (40, 80), "temp": (24, 34), "hum": (50, 80), "ph": (5.5, 7.5), "rain": (800, 2500), "soil": ["Loamy", "Laterite"]},
    "Maize":        {"N": (60,120), "P": (40, 70), "K": (50,100), "temp": (20, 30), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (500, 1000), "soil": ["Alluvial", "Loamy","Black"]},
    "Masoor":       {"N": (10, 40), "P": (20, 50), "K": (10, 40), "temp": (15, 30), "hum": (40, 70), "ph": (6.0, 8.0), "rain": (400, 800), "soil": ["Loamy", "Clay"]},
    "Melon":        {"N": (40, 80), "P": (30, 60), "K": (40, 90), "temp": (20, 35), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (300, 800), "soil": ["Sandy", "Loamy"]},
    "Mesta":        {"N": (40, 80), "P": (30, 60), "K": (40, 80), "temp": (24, 34), "hum": (70, 90), "ph": (5.5, 7.0), "rain": (1000, 2500), "soil": ["Alluvial", "Clay"]},
    "Mungbean":     {"N": (5, 40),  "P": (15, 40), "K": (0, 30),  "temp": (22, 35), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Clay", "Loamy"]},
    "Muskmelon":    {"N": (40, 80), "P": (30, 60), "K": (40, 90), "temp": (22, 35), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (300, 800), "soil": ["Sandy", "Loamy"]},
    "Mothbeans":    {"N": (10, 40), "P": (10, 40), "K": (10, 40), "temp": (25, 35), "hum": (40, 70), "ph": (6.0, 7.5), "rain": (300, 800), "soil": ["Sandy", "Loamy"]},
    "Mustard":      {"N": (30, 70), "P": (20, 50), "K": (30, 60), "temp": (20, 30), "hum": (40, 70), "ph": (6.0, 7.5), "rain": (400, 800), "soil": ["Loamy", "Clay","Alluvial"]},
    "Niger seed":   {"N": (20, 50), "P": (20, 50), "K": (20, 50), "temp": (18, 30), "hum": (50, 70), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Loamy", "Clay"]},
    "Onion":        {"N": (50,100), "P": (40, 70), "K": (40, 90), "temp": (15, 30), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Sandy", "Loamy","Alluvial"]},
    "Orange":       {"N": (50,100), "P": (40, 70), "K": (40, 80), "temp": (20, 32), "hum": (60, 85), "ph": (5.5, 7.0), "rain": (1000, 2500), "soil": ["Loamy", "Laterite"]},
    "Papaya":       {"N": (80,140), "P": (40, 70), "K": (80,150), "temp": (22, 32), "hum": (60, 85), "ph": (5.5, 7.0), "rain": (1000, 2500), "soil": ["Loamy", "Alluvial"]},
    "Pepper":       {"N": (60,120), "P": (40, 80), "K": (60,120), "temp": (20, 30), "hum": (70, 90), "ph": (5.5, 6.8), "rain": (1500, 3000), "soil": ["Loamy", "Clay","Laterite"]},
    "Pigeonpeas":   {"N": (10, 40), "P": (20, 50), "K": (20, 50), "temp": (20, 35), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (400, 1000), "soil": ["Loamy", "Black","Red"]},
    "Potato":       {"N": (80,140), "P": (50, 80), "K": (80,120), "temp": (12, 25), "hum": (60, 80), "ph": (5.5, 6.8), "rain": (500, 800), "soil": ["Sandy", "Loamy","Alluvial"]},
    "Pumpkin":      {"N": (40, 90), "P": (30, 60), "K": (40, 80), "temp": (20, 30), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (500, 1000), "soil": ["Sandy", "Loamy"]},
    "Pomegranate":  {"N": (40, 90), "P": (30, 60), "K": (40, 90), "temp": (20, 32), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (500, 1000), "soil": ["Loamy", "Sandy"]},
    "Radish":       {"N": (40, 80), "P": (30, 60), "K": (30, 60), "temp": (10, 25), "hum": (50, 80), "ph": (6.0, 7.0), "rain": (400, 800), "soil": ["Sandy", "Loamy"]},
    "Ragi":         {"N": (30, 70), "P": (20, 50), "K": (30, 60), "temp": (20, 30), "hum": (40, 70), "ph": (5.5, 7.5), "rain": (700, 1200), "soil": ["Loamy", "Laterite","Sandy","Red"]},
    "Rice":         {"N": (60,120), "P": (40, 70), "K": (50,100), "temp": (20, 35), "hum": (70, 90), "ph": (5.0, 6.8), "rain": (1200, 3000), "soil": ["Clay", "Alluvial"]},
    "Safflower":    {"N": (20, 50), "P": (20, 50), "K": (20, 50), "temp": (20, 30), "hum": (40, 70), "ph": (6.0, 8.0), "rain": (300, 700), "soil": ["Loamy", "Clay"]},
    "Sesamum":      {"N": (20, 50), "P": (20, 50), "K": (20, 50), "temp": (25, 35), "hum": (40, 70), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Loamy", "Sandy","Clay","Red"]},
    "Soyabean":     {"N": (20, 50), "P": (20, 50), "K": (20, 50), "temp": (20, 30), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (600, 1000), "soil": ["Loamy", "Black","Clay"]},
    "Sugarcane":    {"N": (100,180), "P": (50,100), "K": (80,150), "temp": (20, 35), "hum": (70, 90), "ph": (6.0, 7.5), "rain": (1000, 2500), "soil": ["Alluvial", "Loamy","Clay"]},
    "Sunflower":    {"N": (40, 80), "P": (30, 60), "K": (40, 80), "temp": (20, 30), "hum": (40, 70), "ph": (6.0, 7.5), "rain": (400, 800), "soil": ["Loamy", "Clay","Black"]},
    "Squash":       {"N": (40, 80), "P": (30, 60), "K": (40, 80), "temp": (20, 30), "hum": (60, 80), "ph": (6.0, 7.0), "rain": (500, 900), "soil": ["Sandy", "Loamy"]},
    "Spinach":      {"N": (50, 90), "P": (30, 50), "K": (30, 60), "temp": (10, 25), "hum": (60, 80), "ph": (6.0, 7.0), "rain": (400, 800), "soil": ["Sandy", "Loamy"]},
    "Strawberry":   {"N": (50, 90), "P": (40, 60), "K": (40, 80), "temp": (10, 25), "hum": (60, 80), "ph": (5.5, 6.5), "rain": (600, 1200), "soil": ["Loamy", "Sandy"]},
    "Sweet Potato": {"N": (50,100), "P": (40, 70), "K": (50,100), "temp": (20, 30), "hum": (60, 80), "ph": (5.5, 6.8), "rain": (500, 1000), "soil": ["Sandy", "Loamy"]},
    "Tapioca":      {"N": (50,100), "P": (40, 70), "K": (50,100), "temp": (20, 35), "hum": (60, 80), "ph": (5.5, 7.0), "rain": (800, 2000), "soil": ["Loamy", "Laterite"]},
    "Tobacco":      {"N": (40, 90), "P": (30, 60), "K": (40, 80), "temp": (20, 32), "hum": (50, 75), "ph": (5.5, 7.0), "rain": (500, 1000), "soil": ["Sandy", "Loamy","Clay","Alluvial"]},
    "Tomato":       {"N": (50,100), "P": (40, 70), "K": (40, 90), "temp": (20, 30), "hum": (60, 80), "ph": (6.0, 7.0), "rain": (500, 900), "soil": ["Loamy", "Sandy"]},
    "Tur":          {"N": (10, 40), "P": (20, 50), "K": (20, 50), "temp": (20, 35), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (400, 1000), "soil": ["Loamy", "Black","Red"]},
    "Turnip":       {"N": (40, 80), "P": (30, 60), "K": (30, 60), "temp": (10, 25), "hum": (50, 80), "ph": (6.0, 7.0), "rain": (400, 800), "soil": ["Sandy", "Loamy"]},
    "Turmeric":     {"N": (60,120), "P": (40, 80), "K": (40, 90), "temp": (20, 30), "hum": (70, 90), "ph": (5.5, 6.8), "rain": (1000, 2000), "soil": ["Loamy", "Clay"]},
    "Urad":         {"N": (5, 40),  "P": (15, 40), "K": (0, 30),  "temp": (22, 35), "hum": (50, 80), "ph": (6.0, 7.5), "rain": (400, 900), "soil": ["Clay", "Loamy"]},
    "Watermelon":   {"N": (40, 80), "P": (30, 60), "K": (40, 90), "temp": (22, 35), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (300, 800), "soil": ["Sandy", "Loamy"]},
    "Wheat":        {"N": (60,120), "P": (40, 70), "K": (50,100), "temp": (10, 25), "hum": (50, 75), "ph": (6.0, 7.5), "rain": (300, 900), "soil": ["Loamy", "Clay","Black","Alluvial"]},
}

# Generate synthetic data
rows = []
samples_per_crop = 700  # you can change to 100, 500, etc.

for crop, vals in crop_conditions.items():
    for _ in range(samples_per_crop):
        N = random.uniform(*vals["N"])
        P = random.uniform(*vals["P"])
        K = random.uniform(*vals["K"])
        temperature = random.uniform(*vals["temp"])
        humidity = random.uniform(*vals["hum"])
        ph = random.uniform(*vals["ph"])
        rainfall = random.uniform(*vals["rain"])
        soil = random.choice(vals["soil"])  # randomly pick one soil type for the sample

        rows.append([N, P, K, temperature, humidity, ph, rainfall, soil, crop])

# -------------------------
# Save dataset
# -------------------------
df = pd.DataFrame(rows, columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "soil", "label"])
df.to_csv("datasets/Crop_recommendation.csv", index=False)

print(f" Dataset generated successfully with {len(df)} samples and saved to 'datasets/Crop_recommendation.csv'")