
import os
import json
import pdb

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
file_path = os.path.join(app_dir, 'data', 'secrets.json')

def store_secret(key, value):
    secrets = read_secrets(file_path)
    secrets[key] = value
    with open(file_path, 'w') as file:
        json.dump(secrets, file, indent=4)


def read_secrets():
    with open(file_path, 'r') as file:
        secrets = json.load(file)
    return secrets

