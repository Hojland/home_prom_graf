from settings import CPH_ID
import requests
import os


OPENWEATHER_KEY = os.getenv('OPENWEATHER_KEY')


def get_weather(city_id: str):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    response = requests.get(url,
                            params={'id': city_id,
                                    'appid': OPENWEATHER_KEY})
    content = response.json()
    main_type = content['weather'][0]['main']
    description = content['weather'][0]['description']
    pressure = content['main']['pressure']
    humidity = content['main']['humidity']
    windspeed = content['wind']['speed']
    clouds = content['clouds']['all']
    return main_type, description, pressure, humidity, windspeed, clouds
    

if __name__ == "__main__":
    main_type, description, pressure, humidity, windspeed, clouds = get_weather(CPH_ID)