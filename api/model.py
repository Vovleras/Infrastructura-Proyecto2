import ray
from arch import arch_model

# Inicializar Ray localmente
if not ray.is_initialized():
    ray.init()

@ray.remote
def predict_volatility_ray(x, fecha=None):
    model = arch_model(y=x, p=1, q=3).fit(update_freq=5, disp='off')
    forecast = model.forecast(horizon=1).variance.iloc[-1, 0]
    return {"fecha": str(fecha), "varianza": forecast}