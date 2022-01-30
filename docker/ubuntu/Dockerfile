FROM ubuntu:impish-20211015
ARG BOT_TOKEN="${BOT_TOKEN}"
ENV BOT_TOKEN ${BOT_TOKEN}
COPY . /app 
WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r /app/requirements.txt
CMD python3 /app/src/main.py