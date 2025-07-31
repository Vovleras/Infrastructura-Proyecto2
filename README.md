
# Predicción de Volatilidad Financiera con Ray

Este proyecto implementa un sistema distribuido para predicción de volatilidad financiera utilizando modelos GARCH y análisis de Sentiment, con paralelización mediante Ray y una interfaz web interactiva.

## Arquitectura

El proyecto está dividido en tres componentes principales:
- **API Backend** (FastAPI + Ray): Modelos de predicción y procesamiento distribuido
- **Frontend** (React + Vite): Interfaz web interactiva con visualizaciones
- **Ray Cluster**: Sistema distribuido para computación paralela
  
## Requisitos
- Docker y Docker Compose
- Python 3.11+
- Node.js 18+
  
## Acceso
Los servicios estarán disponibles en:
- **Frontend**:  http://23.22.8.172:3000/
- **API**: http://23.22.8.172:8000/docs
- **Ray Dashboard**:  http://23.22.8.172:8265/
  
## Funcionalidades
### 1. Predicción de Volatilidad GARCH
- Modelos GARCH(1,3) distribuidos con Ray
- Análisis de series temporales financieras
- Estrategia de trading basada en volatilidad
- Combinación de señales diarias e intradiarias
  
### 2. Análisis de Sentiment
- Procesamiento paralelo de datos de sentiment de Twitter
- Estrategia de portafolio basada en engagement ratio
- Comparación con benchmark NASDAQ
- Visualización de retornos acumulados
  
## Autores
- **Victoria Andrea Volveras Parra**
- **Emily Nuñez Ordoñez** 
- **Salome Acosta Montaño** 
- **Erik Santiago Amariles Solarte ** 
- **Sheila Valencia Chito** 

