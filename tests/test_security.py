from http import HTTPStatus

'''
Caso por algum motivo não consiga decodificar o token
'''
def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não foi possivel validar as credenciais'}