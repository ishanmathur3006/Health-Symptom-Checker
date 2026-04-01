# 🏥 AI Health Symptom Checker

A full-stack AI-powered web application that predicts diseases based on symptoms using Machine Learning and provides detailed explanations using Large Language Models (LLM).

🔗 **Live Demo:** <https://ai-health-symptom-checker-two.vercel.app>

---

## 🚀 Features

- 🔍 Search and select from 131 symptoms
- 🤖 ML-based disease prediction (Random Forest, 100% accuracy)
- 📊 Top 3 possible conditions with confidence scores
- 💬 AI-generated medical explanation (Groq LLaMA 3.3)
- 📱 Responsive, clean medical-themed UI
- ⚡ Real-time predictions via REST API

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Axios, React-Select |
| Backend | FastAPI, Python |
| ML Model | Scikit-learn (Random Forest) |
| LLM | Groq API (LLaMA 3.3 70B) |
| Deployment | Vercel (Frontend), Render (Backend) |
| Dataset | Kaggle Disease-Symptom Dataset (131 symptoms, 41 diseases) |

---

## 🏗️ Architecture

```
User → React Frontend → FastAPI Backend → ML Model (prediction)
                                        → Groq LLM (explanation)
```

---

## 📁 Project Structure

```
health-symptom-checker/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── model_utils.py       # ML model loading & prediction
│   ├── groq_utils.py        # Groq LLM integration
│   ├── train_model.py       # Model training script
│   ├── requirements.txt     # Python dependencies
│   └── dataset.csv          # Kaggle dataset
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   └── App.css          # Styling
│   └── package.json
└── README.md
```

---

## ⚙️ Local Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

---

## 📊 Model Performance

- **Algorithm:** Random Forest Classifier
- **Dataset:** 4920 samples, 131 features, 41 disease classes
- **Accuracy:** 100% on test set
- **Training time:** < 30 seconds

---

## 👨‍💻 Developer

**Ishan Mathur(2228027)**
B.Tech Computer Science & Systems Engineering
KIIT University, Bhubaneswar

---

## ⚠️ Disclaimer

This application is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.
