
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

## Despliegue en AWS

1. Creación de instancia en EC2 :

  - **Tipo**: t3.large.
  - **Grupos de seguridad**: Reglas de entrada tipo SSH, HTTP, TCP personalizado (Puertos: 8000, 3000, 8265, 10001).
  - **Plataforma**: AWS Amazon Linux.
  - **Key**: Vockey.
  - **Elastic IP**: IPv4 public se configuró como una IP elástica fija (23.22.8.172) conectada a la instancia EC2.
  
2. Conexión de la instancia por medio de EC2 Instance Connect:

  - **Instalar Docker**
    - sudo yum update -y
    - sudo yum install docker -y

- **Iniciar Docker y habilitarlo el arranque**
  - sudo systemctl start docker
  - sudo systemctl enable docker

- **Añadir tu usuario al grupo docker**
  - sudo usermod -aG docker ec2-user

- **Instalar Docker Compose v2**
  - sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  - sudo chmod +x /usr/local/bin/docker-compose

- **Verifica instalación**
  - docker --version
  - docker-compose --version

3. Agregar proyecto a la instancia

- **Clonar Repositorio**
  - git clone https://github.com/Vovleras/Infrastructura-Proyecto2.git

- **Acceder al repositorio**
  - cd Infrastructura-Proyecto2

4. Ejecución proyecto

- **Ejecución Docker Compose**
  - sudo docker-compose up --build -d
  
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
- **Salomé Acosta Montaño** 
- **Erik Santiago Amariles Solarte** 
- **Sheila Valencia Chito** 

