"""
Em vista de não termos o DRY criou-se esse conftest.py
esse arquivo é especial e detectado pelo pytest
que permite definir fixtures que podem ser reutilizadas
em qualquer contexto/módulos de testes em projetos
"""

import pytest
from fastapi.testclient import TestClient
from fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)
