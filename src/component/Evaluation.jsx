
import { useEffect, useState } from "react";

function Evaluation() {
  const [models, setModels] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/evaluation")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch model evaluation");
        return res.json();
      })
      .then(setModels)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const metrics = ["accuracy", "precision", "recall", "f1"];

  const formatMetric = (value) =>
    `${(Number(value) * 100).toFixed(0)}%`;

  if (loading) return <p className="status">Loading model evaluation...</p>;
  if (error) return <p className="status error">{error}</p>;

  return (
    <div className="evaluation-card">
      <h2>Model Performance Comparison</h2>

      <p className="subtitle">
        Comparing the performance of machine learning models.
      </p>

      <div className="table-wrapper">
        <table className="evaluation-table">
          <thead>
            <tr>
              <th>Model</th>
              {metrics.map((metric) => (
                <th key={metric}>
                  {metric === "f1" ? "F1-score" :
                    metric.charAt(0).toUpperCase() + metric.slice(1)}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {Object.entries(models).map(([name, scores]) => (
              <tr key={name}>
                <td>{name}</td>
                {metrics.map((metric) => (
                  <td key={metric}>
                    {formatMetric(scores[metric])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Evaluation;
