from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import ray

# Import local modelGarch
from parallel_ray.models import modelGarch




app = FastAPI()

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