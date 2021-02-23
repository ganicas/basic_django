from enum import Enum

from working_progres.views import RobotMicroServiceDataHandler

from administration.common.logging.setup import logger
from robots_machine.settings import ROBOT_MICRO_SERVICE_CRM_QUEUE, ROBOT_MICRO_SERVICE_CRM_ROUTING_KEY
from proel.settings import ROBOT_MICRO_SERVICE_BROKER_URL
"""

    Kombu Q

"""
from kombu import Connection, Exchange, Queue, Consumer

rabbit_connection = '{}'.format(ROBOT_MICRO_SERVICE_BROKER_URL)
rabbit_url = "{}".format(rabbit_connection)
conn = Connection(rabbit_url)

exchange = Exchange(ROBOT_MICRO_SERVICE_CRM_QUEUE, type="direct")
queue = Queue(
    name=ROBOT_MICRO_SERVICE_CRM_QUEUE,
    exchange=exchange,
    routing_key=ROBOT_MICRO_SERVICE_CRM_ROUTING_KEY
)


def run_kombu_process():
    """

    # Process message

    """
    def process_message(body, message):
        process_importer_database_queue(body)
        message.ack()

    # Drain events from Q
    with Consumer(conn, queues=queue, callbacks=[process_message], accept=['json', 'application/text']):
        while True:
            conn.drain_events()

    with conn.Consumer([queue, exchange], callbacks=[process_message], accept=['json', 'application/text']):
        while True:
            try:
                conn.drain_events(timeout=5)
            except socket.timeout as e:
                logger.info('Timeout event {}'.format(e))


class RobotMicroServiceDataType(Enum):
    AUTO_INDUSTRY_ROBOT = 'AUTO_INDUSTRY_ROBOT'


def process_importer_database_queue(body):
    logger.info('Message {}'.format(body))
    # get type of import and call import accordingly

    try:
        if body.get('type') == RobotMicroServiceDataType.AUTO_INDUSTRY_ROBOT.name:
            robot_handler = RobotMicroServiceDataHandler(body)
            robot_handler.handle_robot_working_progress()
    except Exception as e:
        logger.exception(u'Problem in importer rmq_consumer, error: {}'.format(e))

    return True
