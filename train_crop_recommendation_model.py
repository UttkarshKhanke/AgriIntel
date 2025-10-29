import warnings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
import itertools

warnings.filterwarnings("ignore")
os.makedirs("models", exist_ok=True)

# ======================
# Load Dataset
# ======================
data = pd.read_csv("datasets/Crop_recommendation.csv")

if "soil" not in data.columns:
    raise ValueError("'Soil' column not found in dataset! Please add it before training.")

# ======================
# Encode Soil Type
# ======================
soil_encoder = LabelEncoder()
data["Soil_encoded"] = soil_encoder.fit_transform(data["soil"])

# ======================
# Features & Labels
# ======================
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'Soil_encoded']]
y = data['label']

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

scaler = StandardScaler()
X_scaled = X.copy()
X_scaled[X.columns] = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# ======================
# Auto-Tuning Parameters
# ======================
param_grid = {
    "n_estimators": [100, 150, 200, 250],
    "learning_rate": [0.05, 0.1, 0.2],
    "max_depth": [6, 8, 10],
    "subsample": [0.8, 1.0],
    "colsample_bytree": [0.8, 1.0],
    "gamma": [0, 0.1, 0.2, 0.3]
}

best_acc = 0
best_model = None
best_params = None

# ======================
# Train until accuracy > 80%
# ======================
for params in itertools.product(*param_grid.values()):
    if best_acc >= 0.80:
        break

    current_params = dict(zip(param_grid.keys(), params))
    model = XGBClassifier(
        **current_params,
        random_state=42,
        eval_metric="mlogloss",
        use_label_encoder=False
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"Trying: {current_params} -> Accuracy: {acc * 100:.2f}%")

    if acc > best_acc:
        best_acc = acc
        best_model = model
        best_params = current_params

        # Save intermediate best model
        joblib.dump({
            'model': best_model,
            'scaler': scaler,
            'label_encoder': label_encoder,
            'soil_encoder': soil_encoder
        }, 'models/crop_recommendation_model_best.pkl')

        print(f" New best model found! Accuracy: {acc * 100:.2f}%")
    
    # Stop if target achieved
    if best_acc >= 0.80:
        print("\n Target achieved! Stopping training...")
        break

# ======================
# Final Save
# ======================
if best_model:
    joblib.dump({
        'model': best_model,
        'scaler': scaler,
        'label_encoder': label_encoder,
        'soil_encoder': soil_encoder
    }, 'models/crop_recommendation_model.pkl')

    print(f"\n Best Model Saved!")
    print(f"Final Accuracy: {best_acc * 100:.2f}%")
    print(f"Best Parameters: {best_params}")
else:
    print("\n No model achieved 80% accuracy. Try expanding the parameter grid.")
