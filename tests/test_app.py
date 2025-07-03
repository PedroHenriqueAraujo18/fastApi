
from http import HTTPStatus


def test_helloworld(client):
    
    response  = client.get('/')

    assert response.status_code == HTTPStatus.OK
   
    assert response.json() == {'message': 'Hello World'}

def test_wine_creation(client):

    
    response = client.post('/wine/', json = {
        'name': 'name_wine',
        'price': 0.0,
        'wine_type':'any',
            
        },)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() =={
        'name': 'name_wine',
        'price': 0.0,
        'wine_type':'any',
        'id': 1,
    }

def test_user_creation(client):

    response = client.post( '/users/', json = {
        'username' : 'pedro',
        'email' : 'pedro@example.com',
        'password' : 'secret'
    },)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() =={
        'username' : 'pedro',
        'email' : 'pedro@example.com',
        'id' : 2,
    }
