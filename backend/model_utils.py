import joblib
import numpy as np

# Fix disease name spelling errors from dataset
DISEASE_NAME_FIXES = {
    "Peptic ulcer diseae": "Peptic Ulcer Disease",
    "Dimorphic hemmorhoids(piles)": "Dimorphic Hemorrhoids (Piles)",
    "paralysis (brain hemorrhage)": "Paralysis (Brain Hemorrhage)",
    "hepatitis A": "Hepatitis A",
    "hepatitis B": "Hepatitis B",
    "hepatitis C": "Hepatitis C",
    "hepatitis D": "Hepatitis D",
    "hepatitis E": "Hepatitis E",
}

def fix_disease_name(name: str) -> str:
    return DISEASE_NAME_FIXES.get(name, name)

# Load model artifacts
model = joblib.load("model.pkl")
symptoms_list = joblib.load("symptoms_list.pkl")
label_encoder = joblib.load("label_encoder.pkl")

def predict_disease(symptoms: list[str]):
    # Create input vector
    # NEW - fixes the warning
    import pandas as pd

    input_vector = [1 if s in symptoms else 0 for s in symptoms_list]
    input_df = pd.DataFrame([input_vector], columns=symptoms_list)

    # Predict
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    confidence = round(float(np.max(probabilities)) * 100, 2)

    # Decode label
    disease = fix_disease_name(label_encoder.inverse_transform([prediction])[0])

    # Top 3 possible diseases
    top3_indices = np.argsort(probabilities)[::-1][:3]
    top3 = [
        {
            "disease": fix_disease_name(label_encoder.inverse_transform([i])[0]),
            "confidence": round(float(probabilities[i]) * 100, 2)
        }
        for i in top3_indices
    ]

    return {
        "predicted_disease": disease,
        "confidence": confidence,
        "top3": top3
    }

def get_all_symptoms():
    return symptoms_list