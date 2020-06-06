import time
import logging
import threading
from datetime import datetime  
from datetime import timedelta  
from flask import Flask
from flask_restful import Resource, Api
import Adafruit_DHT
import json
import requests

#Get Config
with open('../config.json') as config:
    data = json.load(config)

print(data)

#Adafruit config
#TODO add config file
sensor_type = Adafruit_DHT.DHT22
sensor_pin_4_inside = 4
sensor_pin_22_outside = 22
sensor_thread_running = True
sensor_retry = True
sensor_group_size = 2

#General config
sensor_grouping_size = 3
sensor_read_delay = 3
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
            'sensor_pin_4_inside':{
                "temperature":last_temperature_1,
                "humidity":last_humdity_1,
                "timestamp":str(last_read_time)
            },
            'sensor_pin_22_outside':{
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

#Endpoint Class
class SensorAll(Resource):
    def get(self):

        global mock_database
        listOfReads = mock_database
        
        arrayOfReadsAsJson = []

        for tuple3 in listOfReads:
            insideT =  tuple3[0].temperature
            insideH =  tuple3[0].humdity
            outsideT =  tuple3[1].temperature
            outsideH =  tuple3[1].humdity
            date =  tuple3[2]

            myjson = {f"{date}":{
                    'sensor_inside':{
                    "temperature":insideT,
                    "humidity":insideH
                    },
                    'sensor_outside':{
                    "temperature":outsideT,
                    "humidity":outsideH
                    }
                }
            }

            arrayOfReadsAsJson.append(myjson)

        return arrayOfReadsAsJson
        
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

def readSensors(sensor_type, sensor_pin_4_inside, sensor_pin_22_outside, bool_sensor_retry):
    # sometimes reads occur when sensor does not have a value to return, rety makes sure a value gets returned.
    # use logging instead later
    # maybe change to not continously retry, if a sensors breaks. maybee try 3-5 times then throw error.
    if sensor_retry == True:
        print("sensor - reading - sensor_pin_4_inside...")
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_4_inside)
        print("sensor - reading - sensor_pin_22_outside...")
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_22_outside)
        print("sensor - reading - finished...")
        return (SensorValue(temperature1,humidity1), SensorValue(temperature2,humidity2), datetime.now()) 
    else:
        humidity1, temperature1 = Adafruit_DHT.read(sensor_type, sensor_pin_4_inside
    )
        humidity2, temperature2 = Adafruit_DHT.read(sensor_type, sensor_pin_22_outside)
        if humidity1 is not None and temperature1 is not None and humidity2 is not None and temperature2 is not None:
            return (SensorValue(temperature1,humidity1), SensorValue(temperature2,humidity2), datetime.now())
        else:
            raise Exception("retry off, not all reads succedded")

# Start new Threads
SensorThread("Sensors", sensor_running_flag, sensor_read_delay, sensor_type, sensor_pin_4_inside, sensor_pin_22_outside, sensor_retry).start()
ApiThread("Api",host, port, debug).start()

print ("api.py ... Exiting Main Thread")