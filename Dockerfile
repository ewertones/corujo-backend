FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

COPY requirements.txt app/ app/
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --timeout 0 --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 1 main:app