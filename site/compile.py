from jinja2 import Environment, FileSystemLoader
import os
import json

from urllib.parse import urlparse

ENV = Environment(loader=FileSystemLoader('./templates'))

# compile entity pages and create the big entity list

entity_names = []
entities = {}

for filename in os.listdir('../entities'):
    if filename not in ['full_list.json','known_addresses.json']:
#        if 'augur' in filename:
            entity_names.append(filename[:-5])

tokens = {}

for entity_name in entity_names:
    fname = '{}.json'.format(entity_name)
    fpath = "../entities/{}.json".format(entity_name)

    print(fpath)

    with open(fpath) as f:
        entity_source = f.read()
        entity = json.loads(entity_source)
        entities[entity_name] = entity

        for net in ['eth', 'kov']:
            if net in entity:
                for t in entity[net]:
                    tokens[t['address']] = t

        template = ENV.get_template('entity.html')
        html = template.render(e = entity, fname=fname, data=entity_source)

        # Write output in the corresponding HTML file
        with open('entities/{}.html'.format(entity_name), 'w') as out_file:
            out_file.write(html)

with open('entities.json', 'w') as out_file:
    out_file.write(json.dumps(entities,indent=2))

# create the index page

file_name = 'index.html'
template = ENV.get_template(file_name)
html = template.render(title='Homepage', entities=entities, token_count = len(tokens))

# Write output in the corresponding HTML file
print ('Writing', file_name)
with open(file_name, 'w') as out_file:
    out_file.write(html)
