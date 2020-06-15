from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

index = 'wattage'

mapping = {
    "mappings": {
        "properties": {
            "datetime": {
                "type": "date" # formerly "string"
            },
            "date": {
                "type": "date"
            },
            "hour": {
                "type": "integer"
            },
            "quantity": {
                "type": "float"
            }
        }
    }
}

def create_index(es: Elasticsearch):
    es.indices.create(index=index, body=mapping)


def es_kwh_injection(kwh: list, es: Elasticsearch):
    for day in kwh:
        for hour in day:
            es_injection(hour, es)

def es_injection(doc: dict, es: Elasticsearch):
    es.index(index=index, body=doc)


def es_injection_bulk(kwh: list, es: Elasticsearch):
    bulk(es, index=index, body=kwh)


