import ray
from arch import arch_model
import pandas as pd

@ray.remote
def predict_volatility_ray(x, fecha=None):
    """
    Función Ray que ejecuta predicción de volatilidad usando modelo GARCH
    """
    try:
        # Asegurar que x es una Serie de pandas
        if not isinstance(x, pd.Series):
            x = pd.Series(x)
        
        # Crear y ajustar el modelo GARCH
        model = arch_model(y=x, p=1, q=3).fit(update_freq=5, disp='off')
        
        # Hacer predicción
        forecast = model.forecast(horizon=1).variance.iloc[-1, 0]
        
        return {
            "fecha": str(fecha), 
            "varianza": float(forecast),
            "status": "success"
        }
    except Exception as e:
        return {
            "fecha": str(fecha),
            "varianza": None,
            "status": "error",
            "error": str(e)
        }
