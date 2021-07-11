import argparse
import json
import logging
import socket
import sys
import threading
import time
from decorators import log

from utilities import load_configs, send_message, get_message
import logs.client_log_config


CONFIGS = dict()
logger = logging.getLogger('client_logger')


def help_text():
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def create_exit_message(account_name):
    return {
        CONFIGS['ACTION']: CONFIGS['EXIT'],
        CONFIGS['TIME']: time.time(),
        CONFIGS['ACCOUNT_NAME']: account_name
    }


@log
def arg_parser(CONFIGS):
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=CONFIGS['DEFAULT_IP_ADDRESS'], nargs='?')
    parser.add_argument('port', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        logger.critical('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        logger.critical(f'Указан недопустимый режим работы {client_mode}, допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


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


def get_user_message(sock, CONFIGS, account_name='Guest'):
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        logger.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        CONFIGS['ACTION']: CONFIGS['MESSAGE'],
        CONFIGS['TIME']: time.time(),
        CONFIGS['ACCOUNT_NAME']: account_name,
        CONFIGS['MESSAGE_TEXT']: message
    }
    logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


def create_message(sock, account_name='Guest'):
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        CONFIGS['ACTION']: CONFIGS['MESSAGE'],
        CONFIGS['SENDER']: account_name,
        CONFIGS['DESTINATION']: to_user,
        CONFIGS['TIME']: time.time(),
        CONFIGS['MESSAGE_TEXT']: message
    }
    logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict, CONFIGS)
        logger.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        logger.critical('Потеряно соединение с сервером.')
        sys.exit(1)


def handle_server_message(message, CONFIG):
    if CONFIG['ACTION'] in message and message[CONFIG['ACTION']] == CONFIG['MESSAGE'] and \
            CONFIG['SENDER'] in message and CONFIG['MESSAGE_TEXT'] in message:
        print(f'Получено сообщение от пользователя '
              f'{message[CONFIG["SENDER"]]}:\n{message[CONFIG["MESSAGE_TEXT"]]}')
        logger.info(f'Получено сообщение от пользователя '
                    f'{message[CONFIG["SENDER"]]}:\n{message[CONFIG["MESSAGE_TEXT"]]}')
    else:
        logger.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def message_from_server(sock, my_username):
    while True:
        try:
            message = get_message(sock, CONFIGS)
            if CONFIGS['ACTION'] in message and message[CONFIGS['ACTION']] == CONFIGS['MESSAGE'] and \
                    CONFIGS['SENDER'] in message and CONFIGS['DESTINATION'] in message \
                    and CONFIGS['MESSAGE_TEXT'] in message and message[CONFIGS['DESTINATION']] == my_username:
                print(f'\nПолучено сообщение от пользователя {message[CONFIGS["SENDER"]]}:'
                      f'\n{message[CONFIGS["MESSAGE_TEXT"]]}')
                logger.info(f'Получено сообщение от пользователя {message[CONFIGS["SENDER"]]}:'
                            f'\n{message[CONFIGS["MESSAGE_TEXT"]]}')
            else:
                logger.error(f'Получено некорректное сообщение с сервера: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            logger.critical(f'Потеряно соединение с сервером.')
            break


def user_interactive(sock, username):
    print(help_text())
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print(help_text())
        elif command == 'exit':
            send_message(sock, create_exit_message(username), CONFIGS)
            print('Завершение соединения.')
            logger.info('Завершение работы по команде пользователя.')
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


def main():
    global CONFIGS
    CONFIGS = load_configs(is_server=False)
    server_address, server_port, client_mode = arg_parser(CONFIGS)

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence_message(CONFIGS), CONFIGS)
        answer = handle_response(get_message(transport, CONFIGS), CONFIGS)
        logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except ConnectionRefusedError:
        logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        client_name = ''
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        logger.debug('Запущены процессы')


if __name__ == '__main__':
    main()
