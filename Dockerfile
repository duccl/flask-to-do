FROM ubuntu:latest
WORKDIR /home/local

COPY . .
RUN chmod 777 app/main.py
RUN apt update
RUN apt install -y python3-pip
RUN pip3 install -r requirements.txt
ENV FLASK_HOST="0.0.0.0"
ENV PRODUCTION=1
ENV TASK_API_VERSION="1.0"
ENTRYPOINT [ "/home/local/entrypoint.sh" ]
EXPOSE 5000