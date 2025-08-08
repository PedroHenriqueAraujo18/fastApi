from fastapi import FastAPI, HTTPException,Depends
from http import HTTPStatus
from  sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from fast_zero.security import (create_token,
                                verify_password,
                                )
from fast_zero.models import User
from fast_zero.schemas import (
    Token
)

app = FastAPI()  # Iniciando uma Aplicação do FastAPI




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







