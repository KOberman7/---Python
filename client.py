from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.bind(('localhost', 8887))
s.listen(5)

msg = 'Привет, сервер'
s.send(msg.encode('utf-8'))
data = s.recv(10000)
print(f'Сообщение от сервера {data.decode("utf-8")} длиной {len(data)} байт')
s.close()