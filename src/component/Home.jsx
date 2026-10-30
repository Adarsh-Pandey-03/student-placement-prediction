import { useState } from "react";
import Analysis from "./Analysis";
import Evaluation from "./Evaluation";

// ==================================================
// 1. FORM FIELD CONFIGURATION
// ==================================================

const fields = [
  {
    name: "CGPA",
    label: "CGPA",
    type: "number",
    min: 0,
    max: 10,
    step: 0.01,
    placeholder: "e.g. 8.5",
    defaultValue: 8.5,
  },
  {
    name: "Internships",
    label: "Number of Internships",
    type: "number",
    min: 0,
    step: 1,
    placeholder: "e.g. 2",
    defaultValue: 1,
  },
  {
    name: "Projects",
    label: "Number of Projects",
    type: "number",
    min: 0,
    step: 1,
    placeholder: "e.g. 4",
    defaultValue: 1,
  },
  {
    name: "Workshops",
    label: "Workshops / Certifications",
    type: "number",
    min: 0,
    step: 1,
    placeholder: "e.g. 3",
    defaultValue: 1,
  },
  {
    name: "AptitudeTestScore",
    label: "Aptitude Test Score",
    type: "number",
    min: 0,
    max: 100,
    step: 1,
    placeholder: "Enter score (0–100)",
    defaultValue: 75,
  },
  {
    name: "SoftSkillsRating",
    label: "Soft Skills Rating",
    type: "number",
    min: 0,
    max: 4,
    step: 0.1,
    placeholder: "Enter rating (0–4)",
    defaultValue: 2.5,
  },
  {
    name: "SSC_Marks",
    label: "SSC Marks (%)",
    type: "number",
    min: 0,
    max: 100,
    step: 0.1,
    placeholder: "Enter SSC percentage",
    defaultValue: 75,
  },
  {
    name: "HSC_Marks",
    label: "HSC Marks (%)",
    type: "number",
    min: 0,
    max: 100,
    step: 0.1,
    placeholder: "Enter HSC percentage",
    defaultValue: 75,
  },
];

// ==================================================
// 2. INITIAL FORM DATA
// ==================================================

const initialData = Object.fromEntries(
  fields.map((field) => [
    field.name,
    field.defaultValue ?? "",
  ])
);

// ==================================================
// 3. HOME COMPONENT
// ==================================================

export default function Home() {
  const [formData, setFormData] = useState(() => ({
    ...initialData,
  }));

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // ==================================================
  // 4. HANDLE INPUT CHANGES
  // ==================================================

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    setResult(null);
  };

  // ==================================================
  // 5. HANDLE FORM SUBMISSION
  // ==================================================

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Convert input values to numbers and validate.
    const payload = {};

    for (const field of fields) {
      const value = formData[field.name];

      // Check for empty fields.
      if (
        value === "" ||
        value === null ||
        value === undefined
      ) {
        setResult({
          error: `Please enter ${field.label}.`,
        });
        return;
      }

      const numericValue = Number(value);

      // Check for valid numeric values.
      if (!Number.isFinite(numericValue)) {
        setResult({
          error: `Please enter a valid number for ${field.label}.`,
        });
        return;
      }

      // Check minimum and maximum limits.
      if (
        (field.min !== undefined &&
          numericValue < field.min) ||
        (field.max !== undefined &&
          numericValue > field.max)
      ) {
        setResult({
          error: `${field.label} must be between ${
            field.min ?? "-∞"
          } and ${field.max ?? "∞"}.`,
        });
        return;
      }

      // Add validated value to the API payload.
      payload[field.name] = numericValue;
    }

    // ==================================================
    // 6. SEND REQUEST TO BACKEND API
    // ==================================================

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Prediction request failed (${response.status})`
        );
      }

      const data = await response.json();

      // Store prediction response.
      setResult(data);
    } catch (error) {
      console.error("Prediction error:", error);

      setResult({
        error:
          "Could not connect to the backend. Please check whether the API is running.",
      });
    } finally {
      setLoading(false);
    }
  };

  // ==================================================
  // 7. HANDLE FORM RESET
  // ==================================================

  const handleReset = () => {
    setFormData({ ...initialData });
    setResult(null);
  };

  // ==================================================
  // 8. COMPONENT UI
  // ==================================================

  return (
    <div className="page">
      <div className="form-card">

        {/* Page Heading */}
        <div className="header">
          <span className="tag">STUDENT ANALYTICS</span>
          <h2>Placement Prediction</h2>
          <p>Enter the student's academic performance and skills details.</p>
        </div>

        {/* Student Details Form */}
        <form onSubmit={handleSubmit}>
          <div className="form-grid">

            {/* Generate Input Fields Dynamically */}
            {fields.map((field) => (
              <div
                className="form-group"
                key={field.name}
              >
                <label htmlFor={field.name}>
                  {field.label}
                </label>

                <input
                  id={field.name}
                  name={field.name}
                  type={field.type}
                  min={field.min}
                  max={field.max}
                  step={field.step}
                  placeholder={field.placeholder}
                  value={formData[field.name]}
                  onChange={handleChange}
                  required
                />
              </div>
            ))}

          </div>

          {/* Form Action Buttons */}
          <div className="actions">
            <button
              type="button"
              className="reset-btn"
              onClick={handleReset}
              disabled={loading}
            >
              Reset
            </button>
            <button
              type="submit"
              className="submit-btn"
              disabled={loading}
            >
              {loading
                ? "Predicting..."
                : "Predict Placement →"}
            </button>
          </div>
        </form>

      
      {/* Prediction Result */}
{result && (
  <div className="result">
    <h3>Prediction Result</h3>

    {/* 1. Decision Tree */}
    <h3>1. Decision Tree</h3>
    {result.error ? (
      <p>{result.error}</p>
    ) : (
      <div className="prediction-details">
        <p>
          <strong>Prediction:</strong>{" "}
          {result.DecisionTreePrediction ?? "Not available"}
        </p>
        <p>
          <strong>Probability:</strong>{" "}
          {result.DecisionTreeProbability ?? "Not available"}
        </p>
      </div>
    )}

    {/* 2. Random Forest */}
    <h3>2. Random Forest</h3>
    {result.error ? (
      <p>{result.error}</p>
    ) : (
      <div className="prediction-details">
        <p>
          <strong>Prediction:</strong>{" "}
          {result.RandomForestPrediction ?? "Not available"}
        </p>
        <p>
          <strong>Probability:</strong>{" "}
          {result.RandomForestProbability ?? "Not available"}
        </p>
      </div>
    )}

    {/* 3. Logistic Regression */}
    <h3>3. Logistic Regression</h3>
    {result.error ? (
      <p>{result.error}</p>
    ) : (
      <div className="prediction-details">
        <p>
          <strong>Prediction:</strong>{" "}
          {result.LogisticRegressionPrediction ?? "Not available"}
        </p>
        <p>
          <strong>Probability:</strong>{" "}
          {result.LogisticRegressionProbability ?? "Not available"}
        </p>
      </div>
    )}

    <Analysis />
    <Evaluation/>
  </div>
 )}

        {/* Footer */}
        <p className="footer">
          Enter accurate details for better predictions.
        </p>
      </div>
     
    </div>
  );
}
