import json
import logging
import socket
import sys
import time
from decorators import log

from utilities import load_configs, send_message, get_message
import logs.client_log_config


# s = socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('localhost', 8887))
# s.listen(5)

CONFIGS = dict()
logger = logging.getLogger('client_logger')


@log
def create_presence_message(account_name):
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    logger.info('Создано сообщение для отправки на сервер')
    return message


@log
def handle_response(message):
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            logger.info('Сообщение успешно обработано')
            return '200 : OK'
        logger.error('Сообщение от сервера не обработано')
        return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


@log
def main():
    global CONFIGS
    CONFIGS = load_configs()
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if not 65535 >= server_port >= 1024:
            raise ValueError
    except IndexError:
        server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = CONFIGS.get('DEFAULT_PORT')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    presence_message = create_presence_message('Guest')
    logger.info('Отправка сообщения серверу')
    send_message(transport, presence_message, CONFIGS)
    response = get_message(transport, CONFIGS)
    hanlded_response = handle_response(response)
    logger.debug(f'Ответ от сервера: {response}')
    logger.info(f'Обработанный ответ от сервера: {hanlded_response}')


if __name__ == '__main__':
    main()
