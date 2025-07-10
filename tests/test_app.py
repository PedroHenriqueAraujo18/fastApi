from http import HTTPStatus
from fast_zero.schemas import  UserPublic

def test_helloworld(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'Hello World'}


def test_update_integretiy_error(client,user):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put( 
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Usuário ou email ja existe'
    }

def test_wine_creation(client):
    response = client.post(
        '/wine/',
        json={
            'name': 'name_wine',
            'price': 0.0,
            'wine_type': 'any',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'name_wine',
        'price': 0.0,
        'wine_type': 'any',
        'id': 1,
    }


def test_user_creation(client):
    response = client.post(
        '/users/',
        json={
            'username': 'pedro',
            'email': 'pedro@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'pedro',
        'email': 'pedro@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': []   
        }
          
'''
A integração com ORM não é direta, portanto usa-se o ConfigDict nos schemas para
a conversão.
'''
def test_read_user_with_users(client,user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users':[user_schema]}

def test_update_user(client,user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado'}
