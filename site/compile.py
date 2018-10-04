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


# compile entity pages

entities = []

for filename in os.listdir('../entities'):
    if filename not in ['full_list.json','known_addresses.json']:
        entities.append(filename[:-5])

for entity_name in entities:
    fpath = "../entities/{}.json".format(entity_name)

    with open(fpath) as f:
        entity = json.loads(f.read())

        fname = '{}.json'.format(entity_name)
        data = json.dumps(json.loads(open('../entities/{}'.format(fname)).read()), indent=2);

        template = ENV.get_template('entity.html')
        html = template.render(e = entity, fname=fname, data=data)

        # Write output in the corresponding HTML file
        with open('entities/{}.html'.format(entity_name), 'w') as out_file:
            out_file.write(html)


tokens = {}

def by_site(token):
#    print(token)
    if 'website' in token:
        return token['website']
    else:
        return ''

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

        tokens[network].sort(key=by_site)

prev = 'NIL'
for t in tokens[network]:
    if 'website' not in t or t['website'] == '':
        continue
    if prev == t['website']:
        t['merge'] = True
    prev = t['website']


for item in PAGE_LIST:
    file_name = item + '.html'
    template = ENV.get_template(file_name)
    html = template.render(title=TITLES[item], tokens=tokens)  #, active_state=state)

    # Write output in the corresponding HTML file
    print ('Writing', file_name)
    with open(file_name, 'w') as out_file:
        out_file.write(html)
