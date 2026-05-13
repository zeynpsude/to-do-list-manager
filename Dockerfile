# Aşama 1: Builder (Gereksinimleri kur)
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Aşama 2: Runner (Çalıştırılabilir hafif imaj)
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*
COPY ./src ./src

# FastAPI'yi uvicorn ile başlat
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]