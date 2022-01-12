# syntax=docker/dockerfile:1
FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD ["python", "./main.py"]