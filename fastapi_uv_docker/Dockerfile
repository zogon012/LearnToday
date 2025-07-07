FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY requirements.txt ./
RUN uv pip install --system --no-cache-dir --requirements requirements.txt && \
    pip install uvicorn

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]