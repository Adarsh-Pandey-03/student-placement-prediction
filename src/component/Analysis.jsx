import React from "react";
import { useState } from "react";

function Analysis(){
    const [selectedModel, setSelectedModel] = useState("Decision Tree");
   return(
     <>
{/* Model Evaluation Charts */}
<div className="evaluation-section">
  <div className="evaluation-header">
    <h2>Model Analysis</h2>
    <p>Explore feature importance and confusion matrix results.</p>
  </div>

  {/* Model Selection */}
  <div className="form-group">
    <label htmlFor="evaluationModel">Select Model</label>
    <select
      id="evaluationModel"
      value={selectedModel}
      onChange={(e) => setSelectedModel(e.target.value)}
    >
      <option value="Decision Tree">Decision Tree</option>
      <option value="Random Forest">Random Forest</option>
      <option value="Logistic Regression">Logistic Regression</option>
    </select>
  </div>

    {/* Confusion Matrix */}
  <div className="chart-card">
    <h3 style={{color:"#122136"}}>Confusion Matrix</h3>
    <img
      key={`matrix-${selectedModel}`}
      src={`http://127.0.0.1:8000/image?model=${encodeURIComponent(selectedModel)}`}
      alt={`${selectedModel} confusion matrix`}
      className="evaluation-image"
    />
  </div>
   

  {/* Feature Importance */}
  <div className="chart-card">
    <h3 style={{color:"#122136"}}>Feature Importance</h3>
    
      <img
        key={`importance-${selectedModel}`}
        src={`http://127.0.0.1:8000/image2?model=${encodeURIComponent(selectedModel)}`}
        alt={`${selectedModel} feature importance`}
        className="evaluation-image"
      />
    
  </div>
</div>
  </>
   )
}
export default Analysis;