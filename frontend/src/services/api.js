const API_BASE_URL = "http://34.228.38.150:8000";

export const apiService = {
  // Verificar salud de la API
  checkHealth: async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  },

  // Obtener predicción de volatilidad
  getVolatilityPrediction: async () => {
    const response = await fetch(`${API_BASE_URL}/predict`);
    if (!response.ok) throw new Error("Error en predicción");
    return response.json();
  },

  // Obtener análisis de sentimientos
  getSentimentAnalysis: async () => {
    const response = await fetch(`${API_BASE_URL}/predictSentiment`);
    if (!response.ok) throw new Error("Error en sentiment");
    return response.json();
  },
};
