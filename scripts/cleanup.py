import os
import json

path = "../tokens/"

for dirname in os.listdir(path):

    for fname in os.listdir(os.path.join(path, dirname)):

        fpath = os.path.join(path, dirname, fname)

        with open(fpath) as f:
            token = json.loads(f.read())

            for k in token:
                if type(token[k]) is str:
                    token[k] = token[k].strip()

                if type(token[k]) is list:
                    for k2 in token[k]:
                        if type(token[k][k2]) is str:
                            token[k][k2] = token[k][k2].strip()

        with open(fpath, "w") as f:
            f.write(json.dumps(token, indent=2))
