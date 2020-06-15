from elasticsearch import Elasticsearch, RequestsHttpConnection
from datetime import timedelta, date
from requests_aws4auth import AWS4Auth
import os
import energinet
import es_utils
import settings
import time


host = 'search-homeelasticsearch-bsvbmdkhq4xi7fcchsp3grmjr4.eu-central-1.es.amazonaws.com'
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BASE_URL = 'https://api.eloverblik.dk/CustomerApi/api'
awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, 'es')
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    scheme='https',
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

if __name__ == "__main__":
    while True:
        token = energinet.get_token(BASE_URL)
        from_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
        to_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        kwh = energinet.get_kwh(BASE_URL, token, from_date, to_date)
        try:
            es_utils.create_index(es)
        except:
            pass
        es_utils.es_kwh_injection(kwh, es)
        time.sleep(24*60*60)