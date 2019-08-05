FROM python:3.7-alpine
RUN apk add --no-cache bash
WORKDIR /code
RUN apk add --no-cache postgresql-dev gcc musl-dev linux-headers git libxml2-dev libxslt-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
