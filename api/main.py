from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import ray

# Import local modelGarch
from parallel_ray.models import modelGarch
from parallel_ray.models import modelSentiment




app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SerieInput(BaseModel):
    serie: List[float]
    fecha: Optional[str] = None

""" @app.post("/predict")
async def predict_volatility(data: SerieInput):
    # Convertir la lista en Serie de pandas
    serie = pd.Series(data.serie)
    
    if serie.isnull().any() or not serie.notna().all():
        raise HTTPException(status_code=400, detail="La serie contiene valores inválidos.")

    # Llamar a Ray
    result_ref = predict_volatility_ray.remote(serie, data.fecha or "sin fecha")
    result = ray.get(result_ref)
    return result """

@app.get("/predict")
async def get_predict():
    try:
        # Crear objeto de la clase Model
        model = modelGarch.Model()
        
        # Verificar conexión Ray antes de ejecutar
        if not model.test_ray_connection():
            raise HTTPException(status_code=500, detail="Error al conectar con Ray.")
        
        # Ejecutar estrategia completa
        retorno = model.run_complete_strategy()
        
        return {"message": "Predicción de volatilidad", "data": retorno}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "API de Predicción de Volatilidad",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict (POST)",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ray_available": ray.is_initialized()}

@app.get("/predictSentiment")
async def get_predict_sentiment():
    try:
        
        model = modelSentiment.ModelSentiment()
        
        # Verificar conexión Ray antes de ejecutar
        if not model.test_ray_connection():
            raise HTTPException(status_code=500, detail="Error al conectar con Ray.")
        
        sentiment_df = model.load_data()
        aggregated_df = model.aggregate_sentiment(sentiment_df)
        filtered_df = model.filtered_sentiment(aggregated_df)
        fixed_dates = model.fixed_dates(filtered_df)
        prices_df = model.parallel_ray_sentiment(sentiment_df)
        portfolio_df = model.portfolio_analysis(prices_df, fixed_dates)
        final_portfolio = model.add_benchmark_comparison(portfolio_df)
        
        # Generar datos del gráfico
        chart_info = model.graphic_engagement_ratio(final_portfolio)
        
        return {
            "message":"Análisis de sentiment completado",
            "data" : {
                "portfolio": final_portfolio.to_dict(),
                "chart_data": chart_info,  # Agregar datos del gráfico
                "total_periods" : len(final_portfolio),
                "date range": {"start": str(final_portfolio.index.min()), "end": str(final_portfolio.index.max())}
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")