FROM python:3.7-alpine

COPY requirements.txt .

RUN apk add --no-cache python-dev gcc musl-dev openssl-dev libxml2-dev libxslt-dev libffi-dev libxml2 libxslt \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && apk del python-dev gcc musl-dev openssl-dev libxml2-dev libxslt-dev libffi-dev



WORKDIR /sensors

COPY . .

CMD [ "python3", "main.py" ]