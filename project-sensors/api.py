import time
import logging
import threading
from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api
import Adafruit_DHT

#Adafruit config
sensor_type = Adafruit_DHT.DHT22
sensor_pin_1 = 4
sensor_pin_2 = 22
sensor_thread_running= True
sensor_retry = True
sensor_group_size = 2

#General config
grouped_read_size = 10
sensor_read_delay = 5

#Running flags
api_running_flag = True
sensor_running_flag = True

#Most recent sensor read values
last_temperature_1 = 0.0
last_temperature_2 = 0.0
last_humdity_1 = 0.0
last_humdity_2 = 0.0
last_read_time = 0.0

#grouped reads
list_sensor_reads = list()

#Mock database
mock_database = list()

#Class
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
#Class
class SensorValue:
  def __init__(self, temperature, humdity):
    self.temperature = temperature
    self.humdity = humdity

#Threading class
class ApiThread(threading.Thread):
    def __init__ (self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print(f"Running : {self.name} thread.")
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(SensorNow,'/sensors/now')
        app.run(host='0.0.0.0', port=80,debug=False)
        print(f"Stopping :{self.name} thread.")

#Threading class
class SensorThread (threading.Thread):
    def __init__(self, name, runningFlag, readDelay, sensortype, pin1, pin2, sensorRetry):
        threading.Thread.__init__(self)
        self.name        = name
        self.runningFlag = runningFlag
        self.readDelay   = readDelay
        self.sensortype  = sensortype
        self.pin1        = pin1
        self.pin2        = pin2
        self.sensorRetry = sensorRetry
    def run(self):
        print(f"Running : {self.name} thread.")
        read(self.name, self.runningFlag, self.readDelay, self.sensortype, self.pin1, self.pin2, self.sensorRetry)
        print(f"Stopping :{self.name} thread.")

def read(threadName, runningFlag, readDelay, sensortype, pin1, pin2, sensorRetry):
    while runningFlag:

        global list_sensor_reads
        global last_temperature_1
        global last_temperature_2
        global last_humdity_1
        global last_humdity_2
        global last_read_time

        readings = readSensors(sensortype, pin1, pin2, sensorRetry)

        list_sensor_reads.append(readings)
        last_temperature_1 = readings[0].temperature
        last_temperature_2 = readings[1].temperature
        last_humdity_1     = readings[0].humdity
        last_humdity_2     = readings[1].humdity
        last_read_time     = readings[2]

        #print(threadName + " list_sensor_reads var:" + str(list_sensor_reads))
        #print(threadName + " last_temperature_1 var:" + str(last_temperature_1))
        #print(threadName + " last_temperature_2 var:" + str(last_temperature_2))
        #print(threadName + " last_read_time var:" + str(last_read_time))
        #print(threadName + " list_sensor_reads var:" + str(len(list_sensor_reads)))
        print("reads: " + len(list_sensor_reads.append))

        #sleep for abit
        time.sleep(readDelay)

def readSensors(sensor_type, sensor_pin_1, sensor_pin_2, bool_sensor_retry):
    # sometimes reads occur when sensor does not have a value to return, rety makes sure a value gets returned.
    if sensor_retry == True:
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_1)
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_2)
        return (SensorValue(humidity1,temperature1), SensorValue(humidity2,temperature2), datetime.now()) 
    else:
        humidity1, temperature1 = Adafruit_DHT.read(sensor_type, sensor_pin_1)
        humidity2, temperature2 = Adafruit_DHT.read(sensor_type, sensor_pin_2)
        if humidity1 is not None and temperature1 is not None and humidity2 is not None and temperature2 is not None:
            return (SensorValue(humidity1,temperature1), SensorValue(humidity2,temperature2), datetime.now())
        else:
            raise Exception("retry off, not all reads succedded")

# Start new Threads
SensorThread("Sensors", sensor_running_flag, sensor_read_delay, sensor_type, sensor_pin_1, sensor_pin_2, sensor_retry).start()
ApiThread("Api").start()

print ("Exiting Main Thread")