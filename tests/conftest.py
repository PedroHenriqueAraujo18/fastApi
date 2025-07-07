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
def mock_db_time():
    return _mock_db_time
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
é um comando  like try finally que quando queremos abrir algo
mas escrevemos nele mas dá algo erro e queremos que execute mesmo
assim sem quebrar a aplicação.

Eventos ORM comuns:
|--------------|----------------|
|Evento	       |Descrição       |
|--------------|----------------|
|before_insert |Antes do INSERT.|
|after_insert  |Depois do INSERT|
|before_update |Antes do UPDATE.|
|after_update  |Depois do UPDATE|
|before_delete |Antes do DELETE.|
|after_delete  |Depois do DELETE|
|-------------------------------|

'''
@contextmanager
def _mock_db_time(*, model, time=datetime(2025,7,7)):
    def fake_time_hook(mapper,connection, target):
        if hasattr(target,'created_at'):
            target.created_at = time
   
    event.listen(model,'before_insert',fake_time_hook)

    yield time

    event.remove(model, 'before_insert',fake_time_hook) 