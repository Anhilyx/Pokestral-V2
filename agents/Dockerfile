FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

ENV PORT=8000
EXPOSE ${PORT}

CMD uvicorn api:app --host 0.0.0.0 --port ${PORT}