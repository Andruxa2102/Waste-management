#!/usr/bin/env python
# coding: utf-8


import os
import json
import base64

FOLDER = '/home/user/notebooks/Work/Waste_management_data/'
files_list = []
list_of_dicts = []

# Получим список json-файлов, полученных по API

with os.scandir(FOLDER) as entries:
    for entry in entries:
        if entry.is_file():
            files_list.append(entry.name)

# Создадим папку для картинок

os.makedirs(FOLDER + 'images',exist_ok=True)

# Цикл перебора файлов

for filename in files_list:
    with open(FOLDER + filename, 'r') as f:
        json_file = json.load(f)
        for i in json_file:
            
# Цикл создания картинок и JSON-файла с описаниями

            for key, value in tuple(i['photo'].items()):
                list_of_dicts.append({key: {'id': i['id'], 'number_pics': len(i['photo'].keys()), 'containers': i['containers']}})
                with open(FOLDER + 'images/' + key,"wb") as f:
                    f.write(base64.decodebytes(value.encode('utf-8')))
                    
# Важная строка - очищает память, без нее падал кернел и ОС убивала процесс

        json_file = None

with open(FOLDER + 'list_of_containers.json', 'w', encoding='utf-8') as file:
    json.dump(list_of_dicts, file, indent=4, ensure_ascii=False)
