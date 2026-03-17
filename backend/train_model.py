import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")
df = df.fillna(0)

# Clean column names
df.columns = df.columns.str.strip()

# Separate features and target
X = df.drop("Disease", axis=1)
y = df["Disease"]

# Encode symptom values (strip whitespace)
X = X.map(lambda x: str(x).strip() if isinstance(x, str) else x)

# Get all unique symptoms
all_symptoms = set()
for col in X.columns:
    all_symptoms.update(X[col].unique())
all_symptoms.discard("0")
all_symptoms.discard(0)
all_symptoms = sorted(list(all_symptoms))

print(f"Total unique symptoms: {len(all_symptoms)}")

# Save symptoms list
joblib.dump(all_symptoms, "symptoms_list.pkl")

# One-hot encode: create binary feature for each symptom
def encode_row(row):
    present = set(str(v).strip() for v in row if str(v).strip() != "0")
    return [1 if s in present else 0 for s in all_symptoms]

X_encoded = pd.DataFrame(
    [encode_row(row) for _, row in X.iterrows()],
    columns=all_symptoms
)

# Encode target labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)
joblib.dump(le, "label_encoder.pkl")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y_encoded, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {acc * 100:.2f}%")

# Save model
joblib.dump(model, "model.pkl")
print("✅ Model saved as model.pkl")
print("✅ Symptoms list saved as symptoms_list.pkl")
print("✅ Label encoder saved as label_encoder.pkl")