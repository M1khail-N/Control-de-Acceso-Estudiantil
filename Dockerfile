FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y gcc build-essential default-libmysqlclient-dev pkg-config netcat-openbsd \
    && apt-get clean

# Crear directorio de la app
WORKDIR /app

# Copiar requirements
COPY requirements.txt /app/

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . /app/

# Copiar entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]