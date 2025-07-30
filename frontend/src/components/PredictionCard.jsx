import React, { useState } from "react";
import { apiService } from "../services/api";
import Chart from "./Chart";

export default function PredictionCard() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiService.getVolatilityPrediction();
      setPrediction(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-card">
      <h2>Predicción GARCH</h2>

      <button
        onClick={handlePredict}
        disabled={loading}
        className="predict-btn"
      >
        {loading ? "Analizando..." : "Generar Predicción"}
      </button>

      {error && <div className="error"> {error}</div>}

      {prediction && (
        <div className="results">
          <h3>Resultados:</h3>
          <Chart data={prediction.data} type="volatility" />
          <div className="summary">
            <p>Total Return: {prediction.data.total_return?.toFixed(2)}%</p>
          </div>
        </div>
      )}
    </div>
  );
}
