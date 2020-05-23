from flask import Flask
from flask_restful import Resource, Api
import Adafruit_DHT
import time

# TODO instead of trying to read sensor values on call
# create 2 threads one for the api and one for the sensors.
# Continuosuly record sensor values.
# return the most recent value.

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN_4 = 4
DHT_PIN_22 = 22

def readSensor(sensor_type, sensor_pin, bool_sensor_retry):
    if bool_sensor_retry == True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, sensor_pin)
        return "Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity)
    else:
        humidity, temperature = Adafruit_DHT.read(sensor_type, sensor_pin)
        if humidity is not None and temperature is not None:
            return "Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity)
        else:
            return "Sensor failure: timing issues or check wires."

app = Flask(__name__)
api = Api(app)

class Sensor(Resource):
    def get(self):
        sensor_1_val = readSensor(DHT_SENSOR, DHT_PIN_4, False)
        sensor_2_val = readSensor(DHT_SENSOR, DHT_PIN_22, False)

        return {
            'sensor1':[
                sensor_1_val
            ],
            'sensor2':[
                sensor_2_val
            ]

        }

api.add_resource(Sensor,'/sensors/now')

# create threads in here
# https://realpython.com/intro-to-python-threading/
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=False)
