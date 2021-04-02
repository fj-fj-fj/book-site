# https://github.com/psycopg/psycopg2/issues/684
# https://github.com/psycopg/psycopg2/issues/684
# https://github.com/pypa/pip/issues/9435

FROM python:3.9.1-alpine as base

FROM base as builder

RUN mkdir /install
RUN apk add --update alpine-sdk \
    && apk add libffi-dev openssl-dev postgresql-dev gcc python3-dev musl-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local
COPY . /app
RUN apk --no-cache add libpq
WORKDIR /app
