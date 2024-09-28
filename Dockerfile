# Usamos una imagen base de Python
FROM python:3.8-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos todos los archivos necesarios al contenedor
COPY . /app/

# Instalamos las dependencias necesarias
RUN pip install -r /app/requirements.txt

# Exponemos los puertos necesarios (5000 para el NameNode y 5001-5003 para los DataNodes)
EXPOSE 5000 5001 5002 5003

# Determinamos si se ejecutará el NameNode o el DataNode basado en una variable de entorno
ENTRYPOINT ["python", "/app/entrypoint.py"]
