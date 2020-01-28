import time
import microbit
import utils
import logging


# maybe use loguru
utils.create_logging('.')

if __name__ == "__main__":

    bme280 = BME280()
    while True:
        # Gather temperature, altitude, pressure and humidity
        temperature, pressure, humidity, altitude = bme280.all()
        print(f'Temperature: {temperature}, Pressure: {pressure}, \
         Humidity: {humidity}, Altitude: {altitude}')
        print(f'Microbit temperature: {microbit.temperature()}')

        # Gather noise
        # Maybe only gather noise as the loudest noise within the last second?
        microbit.sleep(1000)


# TODO
# Gather noise. Maybe only gather noise as the loudest noise within the last second
# Make AWS integration, and store info in database of some sort
# Make a local network metabase application on top of the database

# Colour module is working too