FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y \
    gcc \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    python3-dev \
    build-essential \
    binutils \
    && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "geoalert.wsgi:application", "--bind", "0.0.0.0:8000"]