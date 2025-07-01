from fastapi.testclient import TestClient
from http import HTTPStatus
from fast_zero.app import app


def test_odd_and_even_should_return_two_tuples():
    client = TestClient(app)
    
    response  = client.get('/')

    assert response.status_code == HTTPStatus.OK
    resultado = [[0,2,4,6,8],[1,3,5,7,9]]
    assert response.json() == resultado