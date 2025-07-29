# Usa una imagen base de Python
FROM python:3.11-slim

WORKDIR /app

COPY api/ /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la API con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
