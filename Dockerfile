FROM python:3.10.4-slim-bullseye

RUN mkdir /etc/src/
WORKDIR /etc/src/

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY main.py ./
CMD python3 main.py