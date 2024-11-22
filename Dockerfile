FROM python:3.13.0-alpine3.20 

RUN apk upgrade --no-cache

WORKDIR /home
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY app.py .
COPY listener.py .

ENTRYPOINT [ "/usr/bin/env", "python", "listener.py" ]