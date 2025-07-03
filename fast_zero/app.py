from fastapi import FastAPI
from http import HTTPStatus
from fast_zero.schemas import Message,UserSchema,WineSchema,UserPublic,UserDB,WineDB,UserList
app = FastAPI() #Iniciando uma Aplicação do FastAPI


database_wine = []
database_users = []



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
provido pela classe HTTPStatus da http e o response model
para um modelo de resposta do endpoint definido ,  o para
metro que vem do schemas.py usando pydantic e tendo a 
validação automática

model_dump() é um método de modelos do pydantic que converte o objeto em dicionário. 
Por exemplo, user.model_dump() 
faria a conversão em {'username': 'nome do usuário', 
'password': 'senha do usuário', 'email': 'email do usuário'}.
Os ** querem dizer que o dicionário será desempacotado em parâmetros.
Fazendo com que a chamada seja equivalente a UserDB(username='nome do usuário', 
password='senha do usuário', email='email do usuário', id=len(database) + 1)
'''
@app.post('/users/',status_code = HTTPStatus.CREATED,response_model = UserPublic) 
def create_user(user : UserSchema):
    user_created = UserDB(**user.model_dump(), id=len(database_users)+1)
    database_users.append(user_created)
    return user_created
'''
rota post do wine que retorna o WineDB que ja possui
'''
@app.post('/wine/',status_code = HTTPStatus.CREATED, response_model = WineDB)
def create_wine(wine : WineSchema):
    wine_created = WineDB(**wine.model_dump(),id = len(database_wine)+1)
    database_wine.append(wine_created)
    return wine_created

@app.get('/users/', response_model = UserList)
def users_list():
    return {'users': database_users}
