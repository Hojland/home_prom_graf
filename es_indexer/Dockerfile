FROM python:3.7-alpine

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /es_indexer

COPY . .

CMD [ "python3", "indexer.py" ]