FROM python:3.10-slim

WORKDIR /app
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x wait-for.sh

CMD ["sh", "-c", "./wait-for.sh db:5432 && python manage.py migrate && gunicorn --workers=3 --bind=0.0.0.0:8000 scheduler.wsgi:application"]