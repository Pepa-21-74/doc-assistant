FROM python:3.11-slim

# Устанавливаем системные зависимости для компиляции (нужны для faiss / numpy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Перенаправляем кэш Hugging Face в отдельную папку, чтобы сохранять модели на хосте
ENV HF_HOME=/app/cache/huggingface \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY .env .

EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]