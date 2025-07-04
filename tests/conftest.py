"""
Em vista de não termos o DRY criou-se esse conftest.py
esse arquivo é especial e detectado pelo pytest
que permite definir fixtures que podem ser reutilizadas
em qualquer contexto/módulos de testes em projetos

=======================================================

table_registry.metadata.create_all(engine): cria todas as 
tabelas no banco de dados de teste antes de cada teste que 
usa a fixture session

"""

import pytest
from fastapi.testclient import TestClient
from fast_zero.app import app
from fast_zero.models import table_registry
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
    
    table_registry.metadata.drop_all(engine)