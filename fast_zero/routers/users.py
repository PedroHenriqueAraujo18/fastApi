from fastapi import (FastAPI, 
                     HTTPException,
                     Depends,Query, 
                     APIRouter)
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session
from fast_zero.security import (get_password_hash, 
                                get_current_user)
from fast_zero.models import User
from fast_zero.schemas import (
    FilterPage,
    Message,
    UserSchema,
    UserPublic,
    UserList,

)


'''
Implementação do recurso APIRouter.
O prefix e para agrupar todos os endpoints de users sob o mesmo teto
Em vez de sobrecarregar o principal usa-se isso.
'''
router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]




'''
A classe OAuth2PasswordRequestForm do fastapi gera
automaticamente um forms para solicitar nome e senha
ele sera apresentado no swagger UI e Redoc.

Esse novo endpoint recebe dados do form data que são in
jetados automaticamente graças ao depends e tenta recu
perar um email fornecido

'''



@router.get('/', status_code=HTTPStatus.OK, response_model=Message)
def helloWord():
    """Função Hello World

    Parameters:
    Não possui

    Returns:
    Um dicionário com a chave 'message' contendo o helloworld
    """
    return {'message': 'Hello World'}


"""
Nesse router.post tem a rota, o codigo de status sendo 
provido pela classe HTTPStatus da http e o response model
para um modelo de resposta do endpoint definido ,  o para
metro que vem do schemas.py usando pydantic e tendo a 
validação automática

na parte de session : Session diz que essa função vai 
ser executada antes do valor retornado por get_session
e esse valor sera atribuido a session
"""


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)

def create_user(user: UserSchema,
                session: Session):
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


'''
Os parametros offset e limit são utilizados para paginar os resultatods, é util
em grandes bases de dados

offset -> permite pular um numero especifico antes de fazer a busca oque é para 
navegação

limit -> define o maximo de registros a serem retornados, permitindo o controle 
da quantidade de dados envados na resposta
'''
@router.get('/', response_model=UserList)
def users_list(
    session:Session, 
    filter_users:Annotated[FilterPage,Query()]
):
    users  = session.scalars(select(User).offset(filter_users).limit(filter_users.limit)).all()
    return {'users': users}
    

@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int,
                 user: UserSchema,
                 session : Session,
                 current_user :User):
    
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


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, 
                session: Session,
                current_user:CurrentUser):
    
    if current_user.id !=user_id:
        raise HTTPException(
            status_code = HTTPStatus.FORBIDDEN, detail = 'Sem permissões'
        )
    session.delete(current_user)
    session.commit()
    return {'message': 'Usuário deletado'}
