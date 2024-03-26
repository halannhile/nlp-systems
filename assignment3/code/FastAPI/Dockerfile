# Dockerfile for FastAPI

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Specify the full path to the uvicorn executable
CMD ["/usr/local/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
