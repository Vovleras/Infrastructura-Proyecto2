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

          {/* Métricas del Portfolio */}
          <div className="metrics">
            <div className="metric">
              <span>Períodos:</span>
              <strong>{sentiment.data.total_periods}</strong>
            </div>
            <div className="metric">
              <span>Rango:</span>
              <small>
                {sentiment.data["date range"].start} -{" "}
                {sentiment.data["date range"].end}
              </small>
            </div>
          </div>

          {/* Estadísticas adicionales */}
          <div className="portfolio-stats">
            <h4>📊 Estadísticas del Portfolio:</h4>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Total de Períodos:</span>
                <span className="stat-value">
                  {sentiment.data.total_periods}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Estrategia:</span>
                <span className="stat-value">Twitter Engagement Ratio</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Benchmark:</span>
                <span className="stat-value">NASDAQ (QQQ)</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
