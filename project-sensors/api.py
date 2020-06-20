import time
import json
import os
import logging
import threading
import sensorConfig
import Adafruit_DHT
import sensorLogging
import requests
from gpiozero import CPUTemperature
from   flask         import Flask
from   flask_restful import Api, Resource
from   datetime      import datetime  
from   datetime      import timedelta
import psutil

#Config
config = sensorConfig.config

# Most recent sensor read values, for quick access for sensors/now
last_temperature_inside  = 0.0
last_temperature_outside = 0.0
last_humdity_inside      = 0.0
last_humdity_outside     = 0.0
last_read_datetime       = 0.0

#list of grouped reads, to reduce http requests sent to druid by grouping reads.
list_sensor_reads = list()

def postDruidIngestionTask():
    #This will list all the files in present #working directory
    sensorLogging.logger.info('POST http://localhost:8081 Druid ingestion Task')
    os.system("bin/post-index-task --file data/temp.json --url http://localhost:8081")
    
def writeToFile(content, file_path):
    f = open("./data/ingest.json", "w")
    f.write(toDruidFormattedJson(list_sensor_reads))
    f.close()
    sensorLogging.logger.info('druid data written to ./project-sensors/data/ingest.json')
    sensorLogging.logger.info(
        f'CPU usage: {psutil.cpu_percent()}%, ' +
        f'Temperature: {CPUTemperature().temperature}C, ' +
        f'Memory usage: {psutil.virtual_memory()[2]}%')
    postDruidIngestionTask()


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
                    'inside':{
                        "temperature": last_temperature_inside,
                        "humidity"   : last_humdity_inside
                    },
                    'outside':{
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

#TODO this method is shit fix it
def toDruidFormattedJson(listOfReads):
    arrayOfReadsAsJson = []
    jsonString = ""
    for sensorVal in listOfReads:
        
        timestamp = str(sensorVal[2])

        responseInside = {
            "timestamp"  :timestamp,
            "location"   :"inside",
            "temperature":sensorVal[0].temperature,
            "humidity"   :sensorVal[0].humdity
        }
        responseOutside = {
            "timestamp"  :timestamp,
            "location"   :"outside",
            "temperature":sensorVal[1].temperature,
            "humidity"   :sensorVal[1].humdity
        }

        arrayOfReadsAsJson.append(json.dumps(responseInside))
        arrayOfReadsAsJson.append(json.dumps(responseOutside))

    for item in arrayOfReadsAsJson:
        mystr = str(item)
        if jsonString == "":
            jsonString += mystr 
        else: 
            jsonString = jsonString + "\n" + mystr
    return jsonString

#Threading class
class ApiThread(threading.Thread):
    def __init__ (self, name, host, port, debug):
        threading.Thread.__init__(self)
        self.name  = name
        self.host  = host
        self.port  = port
        self.debug = debug
    def run(self):
        sensorLogging.logger.info(f"Running : {self.name} thread.")
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(SensorNow,'/sensors/now')
        app.run(host=self.host, port=self.port,debug=self.debug)
        sensorLogging.logger.info(f"Stopping :{self.name} thread.")

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

    def run(self):
        sensorLogging.logger.info(f"Running : {self.name} thread.")
        read(self.name, self.runningFlag, self.readDelay, self.sensortype, self.pin1, self.pin2, self.sensorRetry, self.groupingSize)
        sensorLogging.logger.info(f"Stopping :{self.name} thread.")

def read(threadName, runningFlag, readDelay, sensortype, pin1, pin2, sensorRetry, groupingSize):
    while runningFlag:

        global last_temperature_inside
        global last_temperature_outside
        global last_humdity_inside
        global last_humdity_outside
        global last_read_datetime
        global list_sensor_reads

        readings = readSensors(sensortype, pin1, pin2, sensorRetry)

        #set lastest read values
        last_temperature_inside  = readings[0].temperature
        last_temperature_outside = readings[1].temperature
        last_humdity_inside      = readings[0].humdity
        last_humdity_outside     = readings[1].humdity
        last_read_datetime       = readings[2]

        #stick into list of sensor reads
        list_sensor_reads.append(readings)

        #if max group size reached, write to file for druid to pick up
        if len(list_sensor_reads) >= groupingSize:

            #Write to file for druid to ingest
            writeToFile(toDruidFormattedJson(list_sensor_reads),"./data/ingest.json")

            #clear the current group
            list_sensor_reads = list()

        time.sleep(readDelay)

def readSensors(sensor_type, sensor_pin_4_inside, sensor_pin_22_outside, bool_sensor_retry):
    # sometimes reads occur when sensor does not have a value to return, retry makes sure a value gets returned.
    # TODO change to not continously, maybee try 3-5 times then throw error.
    if bool_sensor_retry == True:
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_4_inside)
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor_type, sensor_pin_22_outside)
        sensorLogging.logger.info('Finished Reading Adafruit_DHT.22 sensors on pin (4(inside) and 22(outside))')
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

sensorLogging.logger("Exiting main thread.")