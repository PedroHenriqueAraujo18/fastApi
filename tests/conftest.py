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
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from contextlib import contextmanager
from datetime import datetime

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


'''
Eventos de ORM

Existe um problema , por mais que os testes funcionem e validem, alguns dados que tenham init=False 
são determinados pelo banco(no caso Hora), caso queiramos comparar datas fixas o hook facilitaria.

O sqlalchemy tem um sistema de eventos, conhecidos como hooks, esses 
hooks são blocos de códigos que podem ser inseridos ou removidos antes
e depois de uma operação, podendo modificar os dados antes ou depois de
certas operações serem executadas pelo sqlalchemy

o decorador do contextmanager cria um gerenciador de contexto para que a função
seja usado como um bloco with.

metodos dunder são os metodos que possuem __underline__
ele são usados para definir comportamentos especificos  
de classes, permitindo que suas instâncias interajam 
com funcionalidade interna do python


Oque é um with?

'''
@contextmanager
def _mock_db_time(*, model, time=datetime(2025,7,7)):
    def fake_time_hook(mapper,conn, target):
        if hasattr(target,'created_at'):
            target.created_at = time
        else:
            raise AttributeError("Erro, não foi encontrado tal atributo")   
    event.listen(model,'before_insert',fake_time_hook)

    yield time

    event.remove(model, 'after_insert',fake_time_hook) 