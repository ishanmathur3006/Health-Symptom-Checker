import joblib
import numpy as np

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
    disease = label_encoder.inverse_transform([prediction])[0]

    # Top 3 possible diseases
    top3_indices = np.argsort(probabilities)[::-1][:3]
    top3 = [
        {
            "disease": label_encoder.inverse_transform([i])[0],
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