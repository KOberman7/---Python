import os
import time
import logging.handlers


logger = logging.getLogger('server_logger')
logger.setLevel(logging.DEBUG)


log_file = f'server_logs.log'
path_to_logs = os.path.join(os.getcwd())
path = os.path.join(path_to_logs, log_file)
file_handler = logging.handlers.TimedRotatingFileHandler(path, encoding='utf-8', when='D', interval=1)


LOG_MESSAGE = 'time: {asctime} level: {levelname} module: {module} message: {message}'
formatter = logging.Formatter(LOG_MESSAGE, style='{')

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)