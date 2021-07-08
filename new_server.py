import select
import time
from socket import socket, AF_INET, SOCK_STREAM


def listen_to_socket(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    sock.settimeout(0.2)

    return sock


def main():
    address = ('', 8888)
    clients = []
    sock = listen_to_socket(address)

    while True:
        try:
            conn, addr = sock.accept()
        except OSError as e:
            pass
        else:
            print(f'Получен запрос на подключение от {str(addr)}')
            clients.append(conn)
        finally:
            w = []
            try:
                r, w, e = select.select([], clients, [], 0)
            except Exception as e:
                pass
            s_client = []
            for s_client in w:
                timestr = time.ctime(time.time())
            try:
                s_client.send(timestr.encode('utf-8'))
            except:
                clients.remove(s_client)


print('Сервер запущен')
main()