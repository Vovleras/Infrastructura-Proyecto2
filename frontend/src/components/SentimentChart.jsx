import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function SentimentChart({ data }) {
  if (!data || !data.chart_data || !data.chart_data.data) {
    return (
      <div className="chart-placeholder">
        <h4>Gráfico de Sentimientos</h4>
        <div className="chart-content">
          <p>No hay datos de gráfico disponibles</p>
          <small>Ejecuta el análisis para ver el gráfico</small>
        </div>
      </div>
    );
  }

  const chartData = data.chart_data.data;
  const chartInfo = data.chart_data;

  // Formatear tooltip personalizado
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{`Fecha: ${label}`}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {`${entry.name}: ${entry.value.toFixed(2)}%`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-container">
      <h4>{chartInfo.title}</h4>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            label={{
              value: chartInfo.yAxisLabel || "Return (%)",
              angle: -90,
              position: "insideLeft",
            }}
            tick={{ fontSize: 12 }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />

          {/* Línea del Portfolio */}
          {chartInfo.columns.includes("portfolio_return") && (
            <Line
              type="monotone"
              dataKey="portfolio_return"
              stroke="#8884d8"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6 }}
              name="Portfolio Strategy"
            />
          )}

          {/* Línea del Benchmark (NASDAQ) */}
          {chartInfo.columns.includes("nasdaq_return") && (
            <Line
              type="monotone"
              dataKey="nasdaq_return"
              stroke="#ff7300"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6 }}
              name="NASDAQ Benchmark"
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
