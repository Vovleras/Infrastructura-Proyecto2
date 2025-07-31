import React, { useState } from "react";
import { apiService } from "../services/api";
import SentimentChart from "./SentimentChart";

export default function SentimentCard() {
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiService.getSentimentAnalysis();
      setSentiment(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sentiment-card">
      <h2> Sentiment Analysis</h2>

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="analyze-btn"
      >
        {loading ? "Procesando..." : "Analizar Sentimientos"}
      </button>

      {error && <div className="error"> {error}</div>}

      {sentiment && (
        <div className="results">
          <h3>Portfolio Analysis:</h3>

          {/* Gráfico de Sentimientos */}
          <SentimentChart data={sentiment.data} />
        </div>
      )}
    </div>
  );
}
