from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  

from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session
from fast_zero.models import User

SECRET_KEY ='GAMER'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


'''
A funçao recebe um session que sera criado na get session
retornando uma sessao de Banco de dados, o token e obtido
atravez do header de autorização da request e seja do tipo
bearer.

o credentials_exeception e definida como exceção http que 
é lançada caso de algum problema como 401. o Cabeçalho e 
incluido, indicando que o cliente deve fornecer autenticação

o try tentamos decodificar o JWT usando a key secreta e o algo
ritmo especificado e armazena o token no payload e extraimos o
campo sub e verifica se existe.




'''
def get_current_user(
        session:Session = Depends(get_session),
        token: str = Depends(oauth2_scheme)
):
    credentials_exeception = HTTPException(
        status_code = HTTPStatus.UNAUTHORIZED,
        detail='Não foi possivel validar as credenciais',
        headers={'WWW-Authenticate':'Bearer'}
    )
    try:
        payload = decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        subject_email=payload.get('sub')

        if not subject_email: 
            raise credentials_exeception

    except DecodeError:
        raise credentials_exeception
    user = session.scalar(
        select(User).where(User.email == subject_email)
    )
    if not user: 
        raise credentials_exeception
    return user

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

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