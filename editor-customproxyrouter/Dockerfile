FROM python:3.9-slim

WORKDIR /app

# Install requirements
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create src directory and copy application files
WORKDIR /app/src
COPY src/config.json .
COPY src/app.py .

EXPOSE 80

CMD ["python", "app.py"]
