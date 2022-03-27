FROM python:3.9

WORKDIR /src

COPY ./authz/requirements.txt .

RUN pip install -r requirements.txt

COPY ./authz/src/ .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]