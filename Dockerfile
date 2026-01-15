FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /store_app

COPY req.txt /store_app/
RUN pip install -r req.txt && \
    pip install --upgrade pip


COPY . /store_app/