FROM python:3.8-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000 5001 5002 5003

ENTRYPOINT ["python", "/app/entrypoint.py"]
