import settings
import requests
import os
import jmespath
from datetime import timedelta, date, datetime


DATAHUB_REFRESH_TOKEN_JWT = os.getenv('DATAHUB_REFRESH_TOKEN_JWT')
MAALEPUNKTSID = os.getenv('MAALEPUNKTSID')
WEBADGANG = os.getenv('WEBADGANG')
BASE_URL = 'https://api.eloverblik.dk/CustomerApi/api'


def get_token(base_url: str):
    url = base_url+'/Token'
    headers = {"Authorization": f"Bearer {DATAHUB_REFRESH_TOKEN_JWT}"}
    response = requests.get(url,
                        headers=headers)
    content = response.json()
    return content['result']

def get_kwh(base_url: str, token: str, from_date: str, to_date: str):
    url = base_url+f'/MeterData/GetTimeSeries/{from_date}/{to_date}/Hour'
    headers = {"Authorization": f"Bearer {token}"}
    body = {
	"meteringPoints": {
		"meteringPoint": [MAALEPUNKTSID]
        }
        }
    response = requests.post(url,
                        headers=headers,
                        json=body)
    content = response.json()
    results = jmespath.search('result[0].MyEnergyData_MarketDocument.TimeSeries[0].Period[*].Point[*]', content)
    dates = _dates(from_date, to_date)
    kwh = [_items(dates[i], res) for i, res in enumerate(results)]
    return kwh

def _dates(from_date: str, to_date: str):
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")
    dd = [(from_date + timedelta(days=x)).strftime("%Y-%m-%d") \
        for x in range((to_date-from_date).days)]
    return dd

def _items(date, res):
    positions = [result['position'] for result in res]
    quantities = [result['out_Quantity.quantity'] for result in res]
    items = [_item(date, position, quantity) for position, quantity in zip(positions, quantities)]
    return items

def _item(date, position, quantity):
    hour = str(int(position)-1).rjust(2, '0')
    item = {
        'datetime': datetime.strptime(date+'-'+hour.rjust(2, '0'), "%Y-%m-%d-%H"),
        'date': date, 
        'hour': float(position),
        'quantity': float(quantity)
    }
    return item

if __name__ == "__main__":
    token = get_token(BASE_URL)
    from_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    to_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    kwh = get_kwh(BASE_URL, token, from_date, to_date)
    print(kwh)