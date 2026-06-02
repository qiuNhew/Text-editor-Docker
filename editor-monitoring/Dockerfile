FROM ubuntu:22.04

RUN apt-get update -qy
RUN apt-get install -y python3 python3-pip

WORKDIR /app

RUN pip install flask flask-cors requests

COPY ./src /app/
COPY ./src /config/

EXPOSE 80

CMD ["python3", "app.py"]