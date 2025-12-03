FROM python:3.11-slim

WORKDIR /app

# system deps to compile numpy/pandas if needed (kept minimal)
RUN apt-get update && apt-get install -y build-essential gcc gfortran libatlas-base-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]
