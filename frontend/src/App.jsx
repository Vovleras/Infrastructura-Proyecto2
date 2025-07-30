import React, { useState, useEffect } from "react";
import PredictionCard from "./components/PredictionCard";
import SentimentCard from "./components/SentimentCard";
import { apiService } from "./services/api";
import "./style.css";

function App() {
  const [healthStatus, setHealthStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const health = await apiService.checkHealth();
      setHealthStatus(health);
    } catch (error) {
      console.error("API no disponible:", error);
    }
  };

  return (
    <div className="app">
      <h1>Predicción de Volatilidad Financiera</h1>
      <div className="health-status">
        Estado API: {healthStatus?.status || "Desconectado"}
        {healthStatus?.ray_available && " Ray Activo"}
      </div>

      <main className="dashboard">
        <PredictionCard />
        <SentimentCard />
      </main>
    </div>
  );
}

export default App;
