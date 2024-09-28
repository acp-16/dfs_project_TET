# Usamos una imagen base de Python que está aislada del sistema operativo del host
FROM python:3.8-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos todos los archivos necesarios al contenedor
COPY . /app/

# Instalamos las dependencias manualmente sin restricciones del sistema anfitrión
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exponemos los puertos necesarios
EXPOSE 5000 5001 5002 5003

# Determinamos si se ejecutará el NameNode o el DataNode basado en una variable de entorno
ENTRYPOINT ["python", "/app/entrypoint.py"]
