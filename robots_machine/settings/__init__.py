BROKER_URL = 'amqp://guest:guest@localhost:5672'

ROBOT_MICRO_SERVICE_CRM_QUEUE = 'robot_data_validator'
EXCHANGE = 'robot_data_validator'
ROBOT_MICRO_SERVICE_CRM_ROUTING_KEY = 'robot_data_validator_key'
# ROBOT_MICRO_SERVICE_URL = 'http://importer.selecta.televendcloud.com'
ROBOT_MICRO_SERVICE_URL = 'http://localhost:5000'
GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

DEBUG = False

try:
   from .local import *
except Exception:
   pass
