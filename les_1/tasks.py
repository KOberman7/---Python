"""Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание соответствующих переменных.
 Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных."""

import locale
import subprocess
words = ['разработка', 'сокет', 'декоратор']

for i in words:
    print(f'Слово {i}')
    print(f'Длинна {len(i)}')
    print(f'Тип переменной {type(i)}')

unicodes = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
            '\u0441\u043e\u043a\u0435\u0442', '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

for i in unicodes:
    print(f'Слово {i}')
    print(f'Длинна {len(i)}')
    print(f'Тип переменной {type(i)}')

print('*' * 100)

"""Каждое из слов «class», «function», «method» записать в байтовом
 типе без преобразования в последовательность кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных."""

word_list = [b'class', b'function', b'method']

for i in word_list:
    print(f'Тип переменной {type(i)}')
    print(f'Содержимое {i}')
    print(f'Длинна {len(i)}')

print('*' * 100)

"""Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе."""
# list = [b'attribute', b'класс', b'функция', b'type']
# print(list)
# SyntaxError: bytes can only contain ASCII literal characters. Вывод: слова класс и функция нельзя записать в байтовом типе.

print('*' * 100)

"""Преобразовать слова «разработка», «администрирование», «protocol», «standard»
 из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode)."""

raw_list = ['разработка', 'администрирование', 'protocol', 'standard']

for i in raw_list:
    a = i.encode('utf-8')
    print(a)
    b = bytes.decode(a, 'utf-8')
    print(b)

print('*' * 100)

"""Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на кириллице."""


ping_resurs = [['ping', 'yandex.ru'], ['ping', 'youtube.com']]

for ping_now in ping_resurs:
    ping_process = subprocess.Popen(ping_now, stdout=subprocess.PIPE)
    for line in ping_process.stdout:
        print(line)

print('*' * 100)

"""Создать текстовый файл test_file.txt, заполнить его тремя строками: 
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
 Принудительно открыть файл в формате Unicode и вывести его содержимое."""

raw_string = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w+') as file:
    for i in raw_string:
        file.write(i + '\n')
    file.seek(0)

def_coding = locale.getpreferredencoding()

with open('test_file.txt', encoding=def_coding) as file:
    for el in file:
        print(el, end='')
