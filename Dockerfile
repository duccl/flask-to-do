FROM python:3.9
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./app .
COPY entrypoint.sh .
ENTRYPOINT [ "./entrypoint.sh" ]
EXPOSE 5000