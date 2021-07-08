from socket import *
from subprocess import Popen, CREATE_NEW_CONSOLE

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8888))
p_list = []

while True:
    tm = s.recv(1024)
    user = input("Запустить 10 клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")

    if user == 'q':
        break
    elif user == 's':
        for _ in range(10):
            p_list.append(Popen('python time_client_random.py', creationflags=CREATE_NEW_CONSOLE))

        print(' Запущено 10 клиентов')
        print("Текущее время: %s" % tm.decode('utf-8'))
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()

s.close()
