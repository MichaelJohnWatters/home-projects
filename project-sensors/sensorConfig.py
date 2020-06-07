import json
import Adafruit_DHT

#Class
class SensorConfig:
    def __init__(
        self, host, port,debug,
        sensor_type,
        sensor_pin_4_inside,
        sensor_pin_22_outside,
        sensor_thread_running,
        sensor_retry,
        sensor_grouping_size,
        sensor_read_delay,
        api_running_flag,
        sensor_running_flag):
        self.host                  = host
        self.port                  = port
        self.debug                 = debug   
        self.sensor_type           = sensor_type   
        self.sensor_pin_4_inside   = sensor_pin_4_inside 
        self.sensor_pin_22_outside = sensor_pin_22_outside  
        self.sensor_thread_running = sensor_thread_running 
        self.sensor_retry          = sensor_retry 
        self.sensor_grouping_size  = sensor_grouping_size 
        self.sensor_read_delay     = sensor_read_delay 
        self.api_running_flag      = api_running_flag 
        self.sensor_running_flag   = sensor_running_flag

with open('../config.json') as config_file:
    loadConfig = json.load(config_file)

def sensorType(sensorType):
    if sensorType == "Adafruit_DHT.DHT22":
        return Adafruit_DHT.DHT22
    elif sensorType == "Adafruit_DHT.DHT11":
        return Adafruit_DHT.DHT11
    else:
        print("ERROR: Config Unable to detect sensor type")

config = SensorConfig(
    host                  = loadConfig['sensors']['host'],
    port                  = loadConfig['sensors']['port'],
    debug                 = loadConfig['sensors']['debug'],
    sensor_type           = sensorType(loadConfig['sensors']['sensor_type']),
    sensor_pin_4_inside   = loadConfig['sensors']['sensor_pin_4_inside'],
    sensor_pin_22_outside = loadConfig['sensors']['sensor_pin_22_outside'],
    sensor_thread_running = loadConfig['sensors']['sensor_thread_running'],
    sensor_retry          = loadConfig['sensors']['sensor_retry'],
    sensor_grouping_size  = loadConfig['sensors']['sensor_grouping_size'],
    sensor_read_delay     = loadConfig['sensors']['sensor_read_delay'],
    api_running_flag      = loadConfig['sensors']['api_running_flag'],
    sensor_running_flag   = loadConfig['sensors']['sensor_running_flag']
)




