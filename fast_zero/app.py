from fastapi import FastAPI, HTTPException,Depends
from http import HTTPStatus
from  sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserSchema,
    WineSchema,
    UserPublic,
    UserDB,
    WineDB,
    UserList,
)

app = FastAPI()  # Iniciando uma Aplicação do FastAPI

database_users =[]
database_wine = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def helloWord():
    """Função Hello World

    Parameters:
    Não possui

    Returns:
    Um dicionário com a chave 'message' contendo o helloworld
    """
    return {'message': 'Hello World'}


"""
Nesse app.post tem a rota, o codigo de status sendo 
provido pela classe HTTPStatus da http e o response model
para um modelo de resposta do endpoint definido ,  o para
metro que vem do schemas.py usando pydantic e tendo a 
validação automática

na parte de session : Session diz que essa função vai 
ser executada antes do valor retornado por get_session
e esse valor sera atribuido a session
"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)

def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.username ==user.username) | (User.email == user.email))
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code = HTTPStatus.CONFLICT,
                detail = 'Nome de usuário existente'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code = HTTPStatus.CONFLICT,
                detail = 'Email já cadastrado'
            )
    db_user = User(
        username = user.username,password = user.password, email = user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


"""
rota post do wine que retorna o WineDB que ja possui
"""


@app.post('/wine/', status_code=HTTPStatus.CREATED, response_model=WineDB)
def create_wine(wine: WineSchema):
    wine_created = WineDB(**wine.model_dump(), id=len(database_wine) + 1)
    database_wine.append(wine_created)
    return wine_created


@app.get('/users/', response_model=UserList)
def users_list():
    return {'users': database_users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database_users) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    user_new_id = UserDB(**user.model_dump(), id=user_id)
    database_users[user_id - 1] = user_new_id
    return user_new_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database_users) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    del database_users[user_id - 1]
    return {'message': 'Usuário deletado'}
