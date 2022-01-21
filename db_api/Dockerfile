FROM python:3.9

WORKDIR /src

COPY ./db_api/requirements.txt .

RUN pip install -r requirements.txt

COPY ./db_api/src/ .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]