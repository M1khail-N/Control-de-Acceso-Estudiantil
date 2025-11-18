#!/bin/sh

echo "Esperando a que MySQL esté disponible..."
while ! nc -z db 3306; do
  sleep 1
done

echo "MySQL disponible — ejecutando migraciones..."
python manage.py migrate

echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000