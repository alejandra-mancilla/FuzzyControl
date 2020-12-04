FROM python:3.7.8


COPY . /Worker
WORKDIR /Worker
RUN pip install -r requirements.txt
RUN chmod 644 worker.py