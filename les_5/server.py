import json
import logging
import sys
from socket import *
from utilities import load_configs, get_message, send_message
import logs.server_log_config
from decorators import log

CONFIGS = dict()
logger = logging.getLogger('server_logger')


@log
def handle_message(message):
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        logger.info('Запрос создан')
        return {CONFIGS.get('RESPONSE'): 200}
    logger.error('Запрос провалился')
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    }


@log
def main():
    global CONFIGS
    CONFIGS = load_configs()
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = CONFIGS.get('DEFAULT_PORT')
        if not 65535 >= listen_port >= 1024:
            raise ValueError
    except IndexError:
        print('После -\'p\' необходимо указать порт')
        logger.critical('Не указан порт')
        sys.exit(1)
    except ValueError:
        print(
            'Порт должен быть указан в пределах от 1024 до 65535')
        logger.critical('Неверно указан порт')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После \'a\'- необходимо указать адрес для ')
        logger.critical('Не указан адрес')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(CONFIGS.get('MAX_CONNECTIONS'))

    while True:
        client, client_address = transport.accept()
        try:
            message = get_message(client, CONFIGS)
            response = handle_message(message)
            logger.info('Отправка сообщения клиенту')
            send_message(client, response, CONFIGS)
            client.close()
        except (ValueError, json.JSONDecodeError):
            logger.error('Принято некорретное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()