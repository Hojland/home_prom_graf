from prometheus_client import start_http_server, Gauge
from loguru import logger
import time

from src.tcs3472 import TCS3472
from src.bme280 import BME280
from src import sound, weather_api
from settings import PORT, PULL_TIME, CPH_ID


# Create a metric to track time spent and requests made.
g_temperature = Gauge(
    'bme_temperature', 'Temperature in celsius provided by bme280 sensor', ['room'])
g_humidity = Gauge(
    'bme_humidity', 'Humidity in percents provided by bme280 sensor', ['room'])
g_pressure = Gauge(
    'bme_pressure', 'Pressure in kilopascal provided by bme280 sensor', ['room'])
g_altitude = Gauge(
    'bme_altitude', 'Altitude in meters provided by bme280 sensor', ['room'])

g_time = Gauge('time', 'The time at request', ['room'])

# Outside weather
#g_cph_weather_type = Gauge('openweather_weather_type',
#                           'The type of weather from openweather API', ['city'])
#g_cph_weather_description = Gauge('openweather_weather_descriptiom',
#                                  'The description of the weather from openweather API', ['city'])
g_cph_qnh = Gauge('openweather_qnh',
                  'The sea level pressure from openweather API', ['city'])
g_cph_humidity = Gauge('openweather_humidity',
                       'The humidity from openweather API', ['city'])
g_cph_windspeed = Gauge('openweather_windspeed',
                        'The windspeed from openweather API', ['city'])
g_cph_clouds = Gauge('openweather_clouds',
                     'The percentage of cloud coverage from openweather API', ['city'])


# Colours
g_red = Gauge(
    'tcs_red', 'Red from RGB colour around the tcs3472 sensor', ['room'])
g_blue = Gauge(
    'tcs_blue', 'Red from RGB colour around the tcs3472 sensor', ['room'])
g_green = Gauge(
    'tcs_green', 'Red from RGB colour around the tcs3472 sensor', ['room'])

# Sound (dont know the measure)
g_sound_avg = Gauge('mems_sound_avg', 'Average sound level from the mems microphone', ['room'])
g_sound_loud = Gauge('mems_sound_loud', 'Loudest sound level from the mems microphone', ['room'])

if __name__ == "__main__":

    logger.debug("That's it, beautiful and simple logging!")

    # Start up the server to expose the metrics.
    start_http_server(PORT)

    tcs3472 = TCS3472()
    bme280 = BME280()
    while True:
        # request qnh
        cph_weather_type, cph_weather_description, \
            cph_qnh, cph_humidity, cph_windspeed, \
            cph_clouds = weather_api.get_weather(CPH_ID)
        # Gather temperature, altitude, pressure and humidity from bme280
        temperature, pressure, humidity, altitude = bme280.all(qnh=cph_qnh)
        g_temperature.labels('livingroom').set(temperature)
        g_humidity.labels('livingroom').set(humidity)
        g_pressure.labels('livingroom').set(pressure)
        g_altitude.labels('livingroom').set(altitude)

        # Gather outside values
        #g_cph_weather_type.labels('copenhagen').set(cph_weather_type)
        #g_cph_weather_description.labels(
        #    'copenhagen').set(cph_weather_description)
        g_cph_qnh.labels('copenhagen').set(cph_qnh)
        g_cph_humidity.labels('copenhagen').set(cph_humidity)
        g_cph_windspeed.labels('copenhagen').set(cph_windspeed)
        g_cph_clouds.labels('copenhagen').set(cph_clouds)

        # Gather colours
        colour = tcs3472.get_rgbc()
        g_red.labels('livingroom').set(colour.red)
        g_blue.labels('livingroom').set(colour.blue)
        g_green.labels('livingroom').set(colour.green)

        # Gather noise
        loudest_noise, avg_noiselevel = sound.read_loudest(read_span=1, read_time=PULL_TIME/2)
        g_sound_loud.labels('livingroom').set(loudest_noise)
        g_sound_avg.labels('livingroom').set(avg_noiselevel)

        # Maybe only gather noise as the loudest noise within the last second?
        g_time.labels('livingroom').set_to_current_time()
        time.sleep(PULL_TIME/2) # We also sleep half of pull_time in gathering noise

#TODO
# Move to another database for electricity (postgres)
# Elasticsearch should be for stocking some article stuff instead