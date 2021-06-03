import json

def get_secret(key):
    with open('secrets\secrets.json') as secrets_file:
        secrets = json.loads(secrets_file.read())
    return secrets[key]