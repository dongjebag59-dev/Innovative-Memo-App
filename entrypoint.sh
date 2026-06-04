#!/bin/bash
set -e

echo "▶ DB 마이그레이션..."
python manage.py migrate --noinput

echo "▶ 정적 파일 수집..."
python manage.py collectstatic --noinput

echo "▶ Gunicorn 시작..."
exec gunicorn focus.wsgi \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --log-file - \
    --access-logfile -
