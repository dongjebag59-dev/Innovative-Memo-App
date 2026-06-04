web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn focus.wsgi --bind 0.0.0.0:$PORT --log-file -
