FROM python:3.9.16-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE ${APP_PORT}

WORKDIR /app/api

CMD ["sh", "-c", "python3 manage.py makemigrations; python3 manage.py migrate; python3 manage.py runserver ${APP_IP}:${APP_PORT}"]
