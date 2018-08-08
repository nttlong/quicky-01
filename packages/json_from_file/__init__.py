import json

def load(path):
    with open(path) as f:
        data = json.load(f)
        return data

