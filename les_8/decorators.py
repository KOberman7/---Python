from functools import wraps
import logging
import logs.client_log_config as client_log
import logs.server_log_config as server_log


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(logging.basicConfig(filename='client_logs.log', level=logging.INFO))
        print(logging.basicConfig(filename='server_logs.log', level=logging.INFO))
        print(logging.info(func.__doc__))
        print(f'функция {func.__name__} вызвана из функции main')
        print(f'функция {func.__name__} вызвана из функции main')
        return func(*args, **kwargs)
    return wrapper

