import time
import json
import logging
import requests
import threading
import sensorConfig
import Adafruit_DHT
from   flask         import Flask
from   flask_restful import Api, Resource
from   datetime      import datetime  
from   datetime      import timedelta  

#Config
config = sensorConfig.config

# Most recent sensor read values, for quick access for sensors/now
last_temperature_inside  = 0.0
last_temperature_outside = 0.0
last_humdity_inside      = 0.0
last_humdity_outside     = 0.0
last_read_datetime       = 0.0

#list of grouped reads, to reduce http requests sent to druid.
list_sensor_reads = list()

#Mock database for druid atm
mock_database = list()

#Endpoint Class
class SensorNow(Resource):
    def get(self):

        global last_temperature_inside
        global last_temperature_outside
        global last_humdity_inside
        global last_humdity_outside
        global last_read_datetime

        return {
            str(last_read_datetime):{
                    'sensor_inside':{
                        "temperature": last_temperature_inside,
                        "humidity"   : last_humdity_inside
                    },
                    'sensor_outside':{
                        "temperature": last_temperature_outside,
                        "humidity"   : last_humdity_outside
                    }
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

        # (SensorValue(???,???),SensorValue(???,???), datetime)
        for tuple3 in listOfReads:
            myjson = {f"{tuple3[2]}":{
                    'sensor_inside':{
                        "temperature": tuple3[0].temperature,
                        "humidity"   : tuple3[0].humdity
                    },
                    'sensor_outside':{
                        "temperature": tuple3[1].temperature,
                        "humidity"   : tuple3[1].humdity
                    }
                }
            }

            arrayOfReadsAsJson.append(myjson)

        return arrayOfReadsAsJson
        
#Threading class
class ApiThread(threading.Thread):
    def __init__ (self, name, host, port, debug):
        threading.Thread.__init__(self)
        self.name  = name
        self.host  = host
        self.port  = port
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
    def __init__(self, name, runningFlag, readDelay, sensortype, pin1, pin2, sensorRetry, groupingSize):
        threading.Thread.__init__(self)
        self.name         = name
        self.runningFlag  = runningFlag
        self.readDelay    = readDelay
        self.sensortype   = sensortype
        self.pin1         = pin1
        self.pin2         = pin2
        self.sensorRetry  = sensorRetry
        self.groupingSize = groupingSize

        #sensor_thread_running = config.sensor_thread_running
        #sensor_grouping_size  = config.sensor_grouping_size

    def run(self):
        print(f"Running : {self.name} thread.")
        read(self.name, self.runningFlag, self.readDelay, self.sensortype, self.pin1, self.pin2, self.sensorRetry, self.groupingSize)
        print(f"Stopping :{self.name} thread.")

def read(threadName, runningFlag, readDelay, sensortype, pin1, pin2, sensorRetry, groupingSize):
    while runningFlag:

        global last_temperature_inside
        global last_temperature_outside
        global last_humdity_inside
        global last_humdity_outside
        global last_read_datetime

        global list_sensor_reads
        global mock_database

        readings = readSensors(sensortype, pin1, pin2, sensorRetry)

        #set lastest read values
        last_temperature_inside = readings[0].temperature
        last_temperature_outside = readings[1].temperature
        last_humdity_inside = readings[0].humdity
        last_humdity_outside = readings[1].humdity
        last_read_datetime = readings[2]

        #stick into list of sensor reads
        list_sensor_reads.append(readings)

        #if max group size reached, put in mock db + reset group.
        if len(list_sensor_reads) >= groupingSize:
            for read in list_sensor_reads:
                print(f"Adding: {read} mock database")
                global mock_database
                mock_database.append(read)
                list_sensor_reads = list()
        
        print(f"Current Mock database: {len(mock_database)}")
        #sleep for abit
        time.sleep(readDelay)

def readSensors(sensor_type, sensor_pin_4_inside, sensor_pin_22_outside, bool_sensor_retry):
    # sometimes reads occur when sensor does not have a value to return, retry makes sure a value gets returned.
    # TODO change to not continously, maybee try 3-5 times then throw error.
    if bool_sensor_retry == True:
        print("sensor - reading - sensor_pin_4_inside...")
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_4_inside)
        print("sensor - reading - sensor_pin_22_outside...")
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_22_outside)
        print("sensor - reading - finished...")
        return (SensorValue(temperature1,humidity1), SensorValue(temperature2,humidity2), datetime.now()) 
    else:
        humidity1, temperature1 = Adafruit_DHT.read(sensor_type, sensor_pin_4_inside)
        humidity2, temperature2 = Adafruit_DHT.read(sensor_type, sensor_pin_22_outside)
        if humidity1 is not None and temperature1 is not None and humidity2 is not None and temperature2 is not None:
            return (SensorValue(temperature1,humidity1), SensorValue(temperature2,humidity2), datetime.now())
        else:
            raise Exception("retry off, not all reads succedded")

# Start new Threads
SensorThread(
    "Sensors",
    config.sensor_running_flag,
    config.sensor_read_delay,
    config.sensor_type,
    config.sensor_pin_4_inside,
    config.sensor_pin_22_outside,
    config.sensor_retry,
    config.sensor_grouping_size
    ).start()

ApiThread(
    "Api",
    config.host, 
    config.port, 
    config.debug
).start()

print ("api.py ... Exiting Main Thread")