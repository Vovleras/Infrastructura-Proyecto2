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

export default function Chart({ data, type }) {
  if (!data || !data.chart_data) {
    return <div>No hay datos disponibles</div>;
  }

  return (
    <div className="chart-container">
      <h4>Intraday Strategy Returns</h4>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data.chart_data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            label={{ value: "Returns (%)", angle: -90, position: "insideLeft" }}
          />
          <Tooltip
            formatter={(value) => [`${value.toFixed(2)}%`, "Returns"]}
            labelFormatter={(label) => `Fecha: ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="returns"
            stroke="#8884d8"
            strokeWidth={2}
            dot={false}
            name="Strategy Returns"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
