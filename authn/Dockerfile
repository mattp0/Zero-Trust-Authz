FROM python:3.9

WORKDIR /src

COPY ./authn/requirements.txt .

RUN pip install -r requirements.txt

COPY ./authn/src/ .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]