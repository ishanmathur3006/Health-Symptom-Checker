from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_disease_explanation(disease: str, symptoms: list[str]) -> str:
    symptoms_text = ", ".join(symptoms)
    prompt = f"""
You are a helpful medical assistant. A patient has the following symptoms: {symptoms_text}.
Based on these symptoms, the ML model has predicted the disease: {disease}.

Please provide:
1. A brief, simple explanation of {disease} (2-3 sentences)
2. Why these symptoms match this disease (1-2 sentences)
3. 3 general precautions the patient should take
4. Whether they should see a doctor urgently (yes/no and why)

Keep the response friendly, clear, and easy to understand for a non-medical person.
End with a disclaimer that this is not a substitute for professional medical advice.
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Could not generate explanation at this time. Please consult a doctor for proper diagnosis."