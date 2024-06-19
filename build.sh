#!/bin/bash

echo "============== Iniciando migraciones ==============" 

alembic revision --autogenerate -m "Initial migration"

echo "============= Aplicando migraciones ============="
alembic upgrade head

echo "============= Ejecutando primer scrapy =========="
python scheduler.py