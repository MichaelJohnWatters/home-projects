import time
import logging
import threading
from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api
import Adafruit_DHT
import json
from json import JSONEncoder

#Adafruit config
#TODO add config file
sensor_type = Adafruit_DHT.DHT22
sensor_pin_1 = 4
sensor_pin_2 = 22
sensor_thread_running = True
sensor_retry = True
sensor_group_size = 2

#General config
sensor_grouping_size = 3
sensor_read_delay = 5
host = '0.0.0.0'
port = 80
debug = False

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

#Endpoint Class
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

#Endpoint Class
class SensorAll(Resource):
    def get(self):
        responseObj = SensorValue(10.00, 99.00)
        return responseObj.toJSON()

#Class
class SensorValue:
    def __init__(self, temperature, humdity):
        self.temperature = temperature
        self.humdity = humdity
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

#Threading class
class ApiThread(threading.Thread):
    def __init__ (self, name, host, port, debug):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.debug = debug
    def run(self):

        print(f"Running : {self.name} thread.")

        app = Flask(__name__)
        api = Api(app)

        api.add_resource(SensorNow,'/sensors/now')
        api.add_resource(SensorAll,'/sensors/all')

        app.run(host=self.host, port=self.port,debug=self.debug)

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

        global last_temperature_1
        global last_temperature_2
        global last_humdity_1
        global last_humdity_2
        global last_read_time
        global sensor_grouping_size
        global list_sensor_reads
        global mock_database

        readings = readSensors(sensortype, pin1, pin2, sensorRetry)

        #set lastest read values
        last_temperature_1 = readings[0].temperature
        last_temperature_2 = readings[1].temperature
        last_humdity_1     = readings[0].humdity
        last_humdity_2     = readings[1].humdity
        last_read_time     = readings[2]

        #stick into list of sensor reads
        list_sensor_reads.append(readings)

        #if max group size reached, put in mock db + reset group.
        if len(list_sensor_reads) >= sensor_grouping_size:
            for read in list_sensor_reads:
                print(f"Adding: {read} mock database")
                global mock_database
                mock_database.append(read)
                list_sensor_reads = list()
        
        print(f"Current Mock database: {len(mock_database)}")
        #sleep for abit
        time.sleep(readDelay)

def readSensors(sensor_type, sensor_pin_1, sensor_pin_2, bool_sensor_retry):
    # sometimes reads occur when sensor does not have a value to return, rety makes sure a value gets returned.
    # use logging instead later
    if sensor_retry == True:
        print("sensor - reading - sensor_pin_1...")
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_1)
        print("sensor - reading - sensor_pin_2...")
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_2)
        print("sensor - reading - finished...")
        return (SensorValue(temperature1,humidity1), SensorValue(temperature1,humidity2), datetime.now()) 
    else:
        humidity1, temperature1 = Adafruit_DHT.read(sensor_type, sensor_pin_1)
        humidity2, temperature2 = Adafruit_DHT.read(sensor_type, sensor_pin_2)
        if humidity1 is not None and temperature1 is not None and humidity2 is not None and temperature2 is not None:
            return (SensorValue(temperature1,humidity1), SensorValue(temperature1,humidity2), datetime.now())
        else:
            raise Exception("retry off, not all reads succedded")

# Start new Threads
SensorThread("Sensors", sensor_running_flag, sensor_read_delay, sensor_type, sensor_pin_1, sensor_pin_2, sensor_retry).start()
ApiThread("Api",host, port, debug).start()

print ("api.py ... Exiting Main Thread")