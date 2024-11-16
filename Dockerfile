FROM python:3.13.0-slim-bookworm

RUN apt-get update && apt-get install -y 

WORKDIR /home
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

#ENTRYPOINT [ "/bin/bash" ]