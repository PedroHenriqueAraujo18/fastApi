from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from jwt import encode

SECRET_KEY ='GAMER'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

"""
Essa função cria um token JWT que é usado para autenticar usuários dentro do sistema
ela recebe um dicionário, adiciona um tempo de expiração ao token. O  conjunto disso
formam um payload, e usa a pyjwt pra codificar essas informações ao token que é retor
nado.
"""
def create_token(data : dict):
    to_enconde = data.copy()
    expire = datetime.now(tz = ZoneInfo('UTC')) + timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_enconde.update({'exp': expire})
    encoded_with_jwt = encode(to_enconde, SECRET_KEY,algorithm = ALGORITHM)
    return encoded_with_jwt