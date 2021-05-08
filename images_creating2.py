#!/usr/bin/env python
# coding: utf-8


import json

labels = ['file', 'type']

with open('/home/user/notebooks/Work/Waste_management_data/list_of_containers.json', 'r') as f:
    file = json.load(f)

for num, i in enumerate(file):
    try:
        container_type = str(tuple(tuple(i.values())[0]['containers'].values())[0]['type_id'])
    except AttributeError:
        container_type = '0'
    
    labels.append([tuple(i.keys())[0], container_type])

labels = sorted(labels, key=lambda x: x[0])
labels = '\n'.join([','.join(i) for i in labels])

with open('/home/user/notebooks/Work/Waste_management_data/annot.csv', 'w') as f:
    f.write(labels)
