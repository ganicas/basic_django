import logging
import os
from logging.handlers import TimedRotatingFileHandler

"""

    Logger main script. 
    Script will provide logging for all interfaces :
    INFO, WARN, ERROR, DEBUG

"""

base_path = os.path.dirname(__file__)
file_path_debug = os.path.abspath(os.path.join(base_path, "..", "..", "..", "..", "log/debug.log"))
file_path_info = os.path.abspath(os.path.join(base_path, "..", "..", "..", "..", "log/info.log"))
file_path_error = os.path.abspath(os.path.join(base_path, "..", "..", "..", "..", "log/error.log"))

########################################################################################################################

logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("application")

logger.setLevel(logging.DEBUG)
logger.propagate = False

sh = logging.StreamHandler()
sh.setLevel(logging.ERROR)

sh.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s CONSOLE %(message)s'))
logger.addHandler(sh)

# INFO LOGGER
fh_info = TimedRotatingFileHandler(file_path_info, backupCount=5)
fh_info.setLevel(logging.INFO)
fh_info.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s  %(message)s'))
logger.addHandler(fh_info)

# ERROR LOGGER
fh_error = TimedRotatingFileHandler(file_path_error, backupCount=5)
fh_error.setLevel(logging.ERROR)
fh_error.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
logger.addHandler(fh_error)

# DEBUG LOGGER
fh_debug = TimedRotatingFileHandler(file_path_debug, backupCount=5)
fh_debug.setLevel(logging.DEBUG)
fh_debug.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s  %(message)s'))
logger.addHandler(fh_debug)
