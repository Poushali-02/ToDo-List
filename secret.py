import secrets

key = secrets.token_hex(16)

with open('.env', 'a') as f:
    f.write(f'FLASK_SECRET_KEY={key}')