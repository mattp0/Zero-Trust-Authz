FROM python:3.9

WORKDIR /src

COPY ./client_helper/requirements.txt .

RUN pip install -r requirements.txt

COPY ./client_helper/src/ .

ENTRYPOINT ["tail", "-f", "/dev/null"]