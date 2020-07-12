FROM python:3.7-alpine

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

COPY . /app

RUN pip3 install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

RUN pip3 install -e .

CMD /usr/local/bin/service-monitor