import json

def salvar_token(token):
    with open('token.json', 'w') as file:
        json.dump({'token': token}, file)

def ler_token():
    try:
        with open('token.json', 'r') as file:
            data = json.load(file)
            return data.get('token')
    except FileNotFoundError:
        return None