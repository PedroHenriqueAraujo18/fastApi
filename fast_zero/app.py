from fastapi import FastAPI
from http import HTTPStatus
from fast_zero.schemas import Message
app = FastAPI() #Iniciando uma Aplicação do FastAPI

@app.get('/',status_code=HTTPStatus.OK, response_model=Message) #Definindo um endpoint com o endereço acessivel pelo metodo HTTP GET
def helloWord():
    return{'message':'Hello World'}

@app.post('/users/',status_code = HTTPStatus.CREATED) 
def create_user():
    ...

@app.post('/wine/',status_code = HTTPStatus.CREATED)
def create_wine():
    ...

