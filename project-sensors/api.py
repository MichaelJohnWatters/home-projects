from flask import Flask
from flask_restful import Resource, Api
import Adafruit_DHT
import time
import logging
import threading
from datetime import datetime

# TODO instead of trying to read sensor values on request
# create 2 threads one for the api and one for the sensors.
# Continuosuly record sensor values.
# return the most recent value.
# will eventualy post to druid db.

## Config will have config file
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN_4 = 4
DHT_PIN_22 = 22
sensor_thread_running= True
sensor_retry = True
sensor_group_size = 2

#mock db will be druid
mock_database = list()

#grouped reads
list_sensor_reads = list()

#Quick call vars - /sensors/now
last_temperature_1
last_temperature_2
last_humdity_1
last_humdity_2
last_read_time

#Classes
class SensorNow(Resource):
    def get(self):
        global last_temperature_1
        global last_temperature_2
        global last_humdity_1
        global last_humdity_2
        global last_read_time
        return {
            'sensor1':{
                "temperature":last_temperature_1,
                "humidity":last_humdity_1,
                "timestamp":str(last_read_time)
            },
            'sensor2':{
                "temperature":last_temperature_2,
                "humidity":last_humdity_2,
                "timestamp":str(last_read_time)
            }
        }

class SensorValue:
  def __init__(self, temperature, humdity):
    self.temperature = temperature
    self.humdity = humdity

# Thread -side affect function
# add config
def apiThread():
    app.run(host='0.0.0.0', port=80,debug=False)

# Thread - Side affect function
def sensorsThread(sensor_type, bool_sensor_retry, sensor_dht_pin_one, sensor_dht_pin_two):
    global last_temperature_1
    global last_temperature_2
    global last_humdity_1
    global last_humdity_2
    global last_read_time
    
    while sensor_thread_running == True:
        # check current group size, if too large send to db and reset group.
        if(len(list_sensor_reads) > sensor_group_size):
            #TODO send list of reads to druid + confirm injestion.
            mock_database.append(list_sensor_reads)
            #clear list of reads
            list_sensor_reads = list()

        # read sensors
        sensorValues = readSensors(sensor_type,bool_sensor_retry,sensor_dht_pin_one,sensor_dht_pin_two)
        
        #update quick calls
        last_temperature_1 = sensorValues[0].temperature
        last_temperature_2 = sensorValues[1].temperature
        last_humdity_1 = sensorValues[0].humdity
        last_humdity_2 = sensorValues[1].humdity
        last_read_time = sensorValues[2]

        #append to read grouping
        list_sensor_reads.append(sensorValues)

        #sleep thread
        time.sleep(3)

#returns tuple3 (SensorValue, SensorValue, datetime)        
def readSensors(sensor_type, bool_sensor_retry, sensor1, sensor2):
    if bool_sensor_retry ==True:
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_type, sensor1)
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_type, sensor2)
        if humidity1 is not None and temperature1 is not None and humidity2 is not None and temperature2 is not None :
            return (SensorValue(humidity1,temperature1), SensorValue(humidity2,temperature2), datetime.now())
        else:
            #log message in future
            raise Exception("Sensor failure: timing issues or check wires.")
    else:
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_type, sensor1)
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_type, sensor2)
        return (SensorValue(humidity1,temperature1), SensorValue(humidity2,temperature2), datetime.now())

#def readSensor(sensor_type, sensor_pin, bool_sensor_retry):
#    if bool_sensor_retry == True:
#        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, sensor_pin)
#        return "Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity)
#    else:
#        humidity, temperature = Adafruit_DHT.read(sensor_type, sensor_pin)
#        if humidity is not None and temperature is not None:
#            return "Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity)
#        else:
#            return "Sensor failure: timing issues or check wires."

app = Flask(__name__)
api = Api(app)

api.add_resource(SensorNow,'/sensors/now')

# create threads in here
# https://realpython.com/intro-to-python-threading/
if __name__ == '__main__':
    sensorsThread = threading.Thread(target=sensorsThread, args=())
    apiThread = threading.Thread(target=apiThread, args=())

    sensorsThread.start
    apiThread.start

    

