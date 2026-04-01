import React, { useState, useEffect, useRef } from "react";
import Select from "react-select";
import axios from "axios";
import "./App.css";

const API_BASE = "https://health-symptom-api.onrender.com";

function formatExplanation(text) {
  if (!text) return null;
  const lines = text.split("\n").filter(line => line.trim() !== "");
  return lines.map((line, index) => {
    if (line.match(/^\d+\./)) {
      return (
        <p key={index} style={{ marginBottom: "8px", paddingLeft: "12px", borderLeft: "3px solid #1a73e8" }}>
          {line}
        </p>
      );
    }
    if (line.toLowerCase().includes("disclaimer") || line.toLowerCase().includes("not a substitute")) {
      return (
        <p key={index} style={{ marginTop: "12px", color: "#888", fontStyle: "italic", fontSize: "0.85rem" }}>
          {line}
        </p>
      );
    }
    return <p key={index} style={{ marginBottom: "10px" }}>{line}</p>;
  });
}

function App() {
  const [allSymptoms, setAllSymptoms] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const resultRef = useRef(null);
  const [symptomsLoading, setSymptomsLoading] = useState(true);
  
  useEffect(() => {
    setSymptomsLoading(true);
    axios.get(`${API_BASE}/symptoms`)
      .then(res => {
        const options = res.data.symptoms.map(s => ({
          value: s,
          label: s.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase())
        }));
        setAllSymptoms(options);
        setSymptomsLoading(false);
      })
      .catch(() => {
        setError("Service is waking up... Please wait 30 seconds and refresh.");setSymptomsLoading(false);
      });
  }, []);

  const removeSymptom = (symptom) => {
    setSelectedSymptoms(selectedSymptoms.filter(s => s.value !== symptom));
  };

  const handleClear = () => {
    setSelectedSymptoms([]);
    setResult(null);
    setError("");
  };

  const handlePredict = async () => {
    if (selectedSymptoms.length < 2) {
      setError("Please select at least 2 symptoms for an accurate prediction.");
      return;
    }
    setError("");
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE}/predict`, {
        symptoms: selectedSymptoms.map(s => s.value)
      });
      setResult(response.data);
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 70) return "#2e7d32";
    if (confidence >= 40) return "#f57c00";
    return "#d32f2f";
  };

  return (
    <div className="app">
      {/* Header */}
      <div className="header">
        <h1>🏥 AI Health Symptom Checker</h1>
        <p>Select your symptoms and get an AI-powered disease prediction</p>
      </div>

      {/* Symptom Selector */}
      <div className="card">
        <h2>🔍 Select Your Symptoms
          {selectedSymptoms.length > 0 && (
            <span style={{ marginLeft: "auto", fontSize: "0.8rem", color: "#888" }}>
              {selectedSymptoms.length} selected
            </span>
          )}
        </h2>
        <Select
          options={allSymptoms}
          onChange={(selected) => {
            if (selected && !selectedSymptoms.find(s => s.value === selected.value)) {
              setSelectedSymptoms([...selectedSymptoms, selected]);
              setError("");
            }
          }}
          placeholder={symptomsLoading ? "⏳ Loading symptoms..." : "Search and select a symptom..."}
          value={null}
          isSearchable
          isDisabled={symptomsLoading}
        />

        {selectedSymptoms.length > 0 && (
          <div className="selected-symptoms">
            {selectedSymptoms.map(s => (
              <span key={s.value} className="symptom-tag">
                {s.label}
                <button onClick={() => removeSymptom(s.value)}>×</button>
              </span>
            ))}
          </div>
        )}

        {selectedSymptoms.length > 0 && (
          <button onClick={handleClear} className="clear-btn">
            🗑️ Clear All
          </button>
        )}
      </div>

      {/* Error */}
      {error && <div className="error-msg" style={{ marginTop: "16px" }}>⚠️ {error}</div>}

      {/* Predict Button */}
      <button
        className="predict-btn"
        onClick={handlePredict}
        disabled={loading || selectedSymptoms.length < 2}
      >
        {loading ? (
          <span className="spinner-text">⏳ Analyzing your symptoms...</span>
        ) : (
          "🔎 Check Symptoms"
        )}
      </button>

      {/* Results */}
      {result && (
        <div ref={resultRef}>
          {/* Disease Result */}
          <div className="card" style={{ marginTop: "24px" }}>
            <h2>🦠 Prediction Result</h2>
            <div className="result-disease">
              <div className="disease-name">{result.predicted_disease}</div>
              <div
                className="confidence-badge"
                style={{
                  background: `${getConfidenceColor(result.confidence)}22`,
                  color: getConfidenceColor(result.confidence)
                }}
              >
                {result.confidence}% confidence
              </div>
            </div>

            {/* Top 3 */}
            <div className="top3">
              <h3>📊 Top 3 Possible Conditions</h3>
              {result.top3.map((item, index) => (
                <div key={index} className="top3-item">
                  <span style={{ fontWeight: index === 0 ? "600" : "400", minWidth: "200px" }}>
                    {index + 1}. {item.disease}
                  </span>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <div className="progress-bar-bg">
                      <div
                        className="progress-bar-fill"
                        style={{
                          width: `${item.confidence}%`,
                          background: getConfidenceColor(item.confidence)
                        }}
                      />
                    </div>
                    <span style={{ fontSize: "0.85rem", color: "#666", width: "45px" }}>
                      {item.confidence}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Explanation */}
          <div className="card">
            <h2>💬 AI Medical Explanation</h2>
            <div className="explanation">
              {formatExplanation(result.explanation)}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="disclaimer">
            ⚠️ <strong>Disclaimer:</strong> This tool is for informational purposes only
            and is not a substitute for professional medical advice, diagnosis, or treatment.
            Always consult a qualified healthcare provider.
          </div>
        </div>
      )}
    </div>
  );
}

export default App;