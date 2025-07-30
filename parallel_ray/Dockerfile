# Dockerfile para Ray con Python 3.11
FROM python:3.11

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements para instalar dependencias
COPY requirements.txt /app/

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer puertos necesarios para Ray
EXPOSE 8265 10001 6379

# Comando para iniciar Ray
CMD ["ray", "start", "--head", "--block", "--dashboard-host", "0.0.0.0", "--port=6379", "--dashboard-port=8265", "--ray-client-server-port=10001"]
