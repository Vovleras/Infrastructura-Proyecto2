from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import ray
from model import predict_volatility_ray

app = FastAPI()

class SerieInput(BaseModel):
    serie: List[float]
    fecha: Optional[str] = None

@app.post("/predict")
async def predict_volatility(data: SerieInput):
    # Convertir la lista en Serie de pandas
    serie = pd.Series(data.serie)
    
    if serie.isnull().any() or not serie.notna().all():
        raise HTTPException(status_code=400, detail="La serie contiene valores inválidos.")

    # Llamar a Ray
    result_ref = predict_volatility_ray.remote(serie, data.fecha or "sin fecha")
    result = ray.get(result_ref)
    return result