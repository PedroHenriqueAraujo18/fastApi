from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus
from  sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from fast_zero.security import (get_password_hash,
                                create_token,
                                verify_password,
                                get_current_user)
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserSchema,
    WineSchema,
    UserPublic,
    WineDB,
    UserList,
    Token
)

app = FastAPI()  # Iniciando uma Aplicação do FastAPI


database_wine = []



'''
A classe OAuth2PasswordRequestForm do fastapi gera
automaticamente um forms para solicitar nome e senha
ele sera apresentado no swagger UI e Redoc.

Esse novo endpoint recebe dados do form data que são in
jetados automaticamente graças ao depends e tenta recu
perar um email fornecido

'''
@app.post('/token',response_model=Token)
def login_for_access_token(
    form_data : OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Email ou senha incorretas'
        )
    if not verify_password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Email ou senha incorretas'
        )
    access_token = create_token(data={'sub':user.email})

    return {'access_token':access_token,'token_type':'bearer'}




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
        
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username = user.username,
        password =hashed_password,
        email = user.email
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

'''
Os parametros offset e limit são utilizados para paginar os resultatods, é util
em grandes bases de dados

offset -> permite pular um numero especifico antes de fazer a busca oque é para 
navegação

limit -> define o maximo de registros a serem retornados, permitindo o controle 
da quantidade de dados envados na resposta
'''
@app.get('/users/', response_model=UserList)
def users_list(
    skip : int = 0, limit: int = 100, session : Session = Depends(get_session)
):
    users  = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}
    

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int,
                 user: UserSchema,
                 session : Session = Depends(get_session),
                 current_user :User = Depends(get_current_user)):
    
    if current_user.id !=user_id:
        raise HTTPException(
            status_code = HTTPStatus.FORBIDDEN, detail = 'Sem permissões suficientes'
        )
    try :
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)
        return current_user
    except IntegrityError:
             raise HTTPException(
            status_code=HTTPStatus.CONFLICT, 
            detail='Usuário ou email ja existe'
        )


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, 
                session: Session = Depends(get_session),
                current_user:User  =Depends(get_current_user)):
    
    if current_user.id !=user_id:
        raise HTTPException(
            status_code = HTTPStatus.FORBIDDEN, detail = 'Sem permissões'
        )
    session.delete(current_user)
    session.commit()
    return {'message': 'Usuário deletado'}
