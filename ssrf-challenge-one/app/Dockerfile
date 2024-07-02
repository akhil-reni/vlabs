# Pull base image
FROM python:3.12.4-slim

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ENV FLASK_APP=/usr/src/app/proxy.py

CMD ["flask", "run", "--host=0.0.0.0"]
