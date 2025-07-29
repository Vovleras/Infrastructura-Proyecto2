FROM python:3.9-slim


WORKDIR /app

# Copiar primero los requirements
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Luego copiar el código fuente
COPY api/ /app

# Expone el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la API con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
