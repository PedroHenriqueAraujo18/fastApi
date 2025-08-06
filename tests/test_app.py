from http import HTTPStatus
from jwt import decode
from fast_zero.schemas import  UserPublic
from fast_zero.security import SECRET_KEY, create_token
def test_helloworld(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'Hello World'}


def test_update_integretiy_error(client,user,token):
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
        headers={'Authorization': f'Bearer {token}'},
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

def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado'}

def  test_jwt():
    data = {'test':'test'}
    token = create_token(data)
    decoded = decode(token,SECRET_KEY,algorithms=['HS256'])
    assert decoded['test'] == data['test']
    assert 'exp' in decoded

def test_get_token(client,user):
    response = client.post(
        '/token',
        data={'username':user.email,'password':user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token