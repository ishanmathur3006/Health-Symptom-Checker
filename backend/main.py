from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model_utils import predict_disease, get_all_symptoms
from groq_utils import get_disease_explanation

app = FastAPI(title="Health Symptom Checker API")

# Allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomsInput(BaseModel):
    symptoms: list[str]

@app.get("/")
def root():
    return {"message": "Health Symptom Checker API is running!"}

@app.get("/symptoms")
def symptoms():
    return {"symptoms": get_all_symptoms()}

@app.post("/predict")
def predict(input: SymptomsInput):
    if not input.symptoms:
        return {"error": "Please provide at least one symptom"}

    if len(input.symptoms) < 2:
        return {"error": "Please provide at least 2 symptoms for accurate prediction"}

    # Get ML prediction
    result = predict_disease(input.symptoms)

    # Get groq explanation
    explanation = get_disease_explanation(
        result["predicted_disease"],
        input.symptoms
    )

    return {
        "predicted_disease": result["predicted_disease"],
        "confidence": result["confidence"],
        "top3": result["top3"],
        "explanation": explanation
    }