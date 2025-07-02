from fastapi import FastAPI
from http import HTTPStatus
from fast_zero.schemas import Message,UserSchema,WineSchema
app = FastAPI() #Iniciando uma Aplicação do FastAPI



@app.get('/',status_code=HTTPStatus.OK, response_model=Message) 
def helloWord():
    """Função Hello World

    Parameters:
    Não possui
    
    Returns:
    Um dicionário com a chave 'message' contendo o helloworld
    """
    return{'message':'Hello World'}



'''
Nesse app.post tem a rota, o codigo de status sendo 
provido pela classe HTTPStatus da http , e tem o para
metro que vem do schemas.py usando pydantic e tendo a 
validação automática
'''
@app.post('/users/',status_code = HTTPStatus.CREATED) 
def create_user(user : UserSchema):
    ...

@app.post('/wine/',status_code = HTTPStatus.CREATED)
def create_wine(wine : WineSchema):
    ...

