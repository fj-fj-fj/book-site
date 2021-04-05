FROM python:3.9.1-alpine as base

FROM base as builder

ENV PYTHONUNBUFFERED 1

ARG REQUIREMENT_FILE_NAME
ENV REQUIREMENT_FILE_NAME=$REQUIREMENT_FILE_NAME

RUN mkdir /install
RUN apk add --update alpine-sdk \
    && apk add libffi-dev openssl-dev postgresql-dev gcc python3-dev musl-dev cargo

WORKDIR /install

COPY ./requirements /requirements
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --prefix=/install --no-cache-dir -r /requirements/$REQUIREMENT_FILE_NAME

FROM base

COPY --from=builder /install /usr/local
COPY . /app
RUN apk --no-cache add libpq

WORKDIR /app
