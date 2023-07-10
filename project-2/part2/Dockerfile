FROM python:3.9.16-alpine

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

WORKDIR /app/api

CMD ["sh", "-c", "python3 manage.py makemigrations; python3 manage.py migrate; python3 manage.py runserver 0.0.0.0:8000"]
