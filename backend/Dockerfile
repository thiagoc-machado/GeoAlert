FROM python:3.11-slim

# Variáveis para ambiente não-interativo e timezone
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Madrid

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update \
  && apt-get install -y gcc libpq-dev gdal-bin python3-dev \
  && apt-get clean

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Expõe a porta padrão do Gunicorn
EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
