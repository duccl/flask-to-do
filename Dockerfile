FROM ubuntu
WORKDIR /app
RUN apt-get update -y && apt-get install python3 -y
RUN apt-get install libpq-dev python3-dev -y
RUN apt-get install python3-psycopg2 -y
COPY requirements.txt .
RUN apt install python3-pip -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./app .
COPY entrypoint.sh .
ENTRYPOINT [ "./entrypoint.sh" ]
EXPOSE 5000