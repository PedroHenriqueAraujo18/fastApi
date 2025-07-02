from fastapi.testclient import TestClient
from http import HTTPStatus
from fast_zero.app import app


def test_helloworld():
    client = TestClient(app)
    
    response  = client.get('/')

    assert response.status_code == HTTPStatus.OK
    resultado ='Hello World'
    assert response.json() == resultado