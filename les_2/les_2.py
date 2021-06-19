import json
import chardet
import csv
import os
import yaml

# 1
import re


def get_encoding(file):
    raw_data = open(file, 'rb').read()
    result = chardet.detect(raw_data)
    encod = result['encoding']
    return encod


def get_data(files: list):
    headers = ['Изготовитель ОС', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = [headers]

    for file in files:
        with open(file, 'r', encoding=get_encoding(file)) as file:
            file_data = file.read()

        data_row = list()
        for line in file_data.split('\n'):
            for header in headers:
                row_item = re.findall(r'{}:\s+(.+)$'.format(header), line)
                if row_item:
                    data_row.append(row_item[0])

        main_data.append(data_row)

    return main_data


def write_csv(file, data_files):
    data = get_data(data_files)
    with open(file, 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow(row)


path = os.path.join(os.getcwd(), 'lesson_files')

files_txt = [os.path.join(path, file) for file in os.listdir(
    path) if re.findall(r'\.txt$', file)]
files_json = [os.path.join(path, file) for file in os.listdir(
    path) if re.findall(r'\.json$', file)]

#write_csv('my_file.csv', files_txt)

# 2


def write_order_to_json(file, new):
    with open(file, 'r', encoding=get_encoding(file)) as j_file:
        raw_data = json.load(j_file)

    raw_data['orders'].append(new)
    with open(file, 'w', encoding=get_encoding(file)) as j_file:
        json.dump(raw_data, j_file, indent=4)


new_order = {'item': 'dishwasher', 'quantity': 1,
             'price': 2000, 'buyer': 'Alex', 'date': '19.06.2021'}

#write_order_to_json(files_json, new_order)

# 3
currency_signs = {'DOLLAR_SIGN': '\u0024',
                  'RUBLE_SIGN': '\u20BD', 'BITCOIN_SIGN': '\u20BF'}
data = {'list': [3, 6, 7], 'integer': 84, 'currency_signs': currency_signs}

with open('file.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as file:
    file_content = yaml.load(file)

print(file_content)
