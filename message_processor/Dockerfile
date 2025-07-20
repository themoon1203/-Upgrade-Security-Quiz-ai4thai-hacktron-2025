FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Note: port จะ override จาก docker-compose
CMD ["uvicorn", "main:create_app", "--factory", "--host", "0.0.0.0", "--port", "5001"]