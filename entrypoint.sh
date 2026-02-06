
set -e

mkdir -p /app/staticfiles

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running migrate..."
python manage.py migrate --noinput

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-3000} --workers 2
