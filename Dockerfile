FROM ubuntu:latest
ARG BOT_TOKEN="${BOT_TOKEN}"
ENV BOT_TOKEN ${BOT_TOKEN}
WORKDIR /app
COPY . /app 
RUN apt-get update && apt-get install -y python3-pip python-dev build-essential
RUN pip3 install -r /app/requirements.txt
CMD python3 /app/src/main.py