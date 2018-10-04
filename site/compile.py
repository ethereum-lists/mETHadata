from jinja2 import Environment, FileSystemLoader
import os
import json

ENV = Environment(loader=FileSystemLoader('./templates'))

PAGE_LIST = ['index']
TITLES = { 
        'index': 'Methadata'
}

TOKEN_LIST = {
    'eth': [
        '0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C',
        '0xE41d2489571d322189246DaFA5ebDe1F4699F498',
        '0xa74476443119A942dE498590Fe1f2454d7D4aC0d',
    ]
}

entity_name = 'augur'
fpath = "../entities/{}.json".format(entity_name)

with open(fpath) as f:
    entity = json.loads(f.read())

    file_name = 'entity.html'
    template = ENV.get_template(file_name)
    html = template.render(e = entity)

    # Write output in the corresponding HTML file
    print ('Writing', file_name)
    with open(file_name, 'w') as out_file:
        out_file.write(html)


tokens = {}

for network in TOKEN_LIST:
    tokens[network] = []

#    for token_addr in TOKEN_LIST[network]:
    path = "../tokens/"
#    fpath = os.path.join(path, network, token_addr+".json")

#        for dirname in os.listdir(path):
    for fname in os.listdir(os.path.join(path, network)):
        fpath = os.path.join(path, network, fname)

        with open(fpath) as f:
            token = json.loads(f.read())
            tokens[network].append(token)


for item in PAGE_LIST:
    file_name = item + '.html'
    template = ENV.get_template(file_name)
    html = template.render(title=TITLES[item], tokens=tokens)  #, active_state=state)

    # Write output in the corresponding HTML file
    print ('Writing', file_name)
    with open(file_name, 'w') as out_file:
        out_file.write(html)
