FROM python:3.11

WORKDIR /app

# Copiar requirements primero
COPY api/requirements.txt /app/api/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/api/requirements.txt

# Copiar todo el proyecto (api + parallel_ray)
COPY . .

# Expone el puerto
EXPOSE 8000

# Ejecuta con uvicorn como módulo, desde el root con hot-reload para desarrollo
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
