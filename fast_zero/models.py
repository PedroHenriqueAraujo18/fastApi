from datetime import datetime
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            registry)
from sqlalchemy import func

''' Mapped nesse caso significa que o atributo é associado a uma coluna
especifica em tabela de dados 

__tablename__ é o identificador da tabela

para definir propriedades especificas das tabelas utilize o mapped_column


Init = false, significa que quando o objeto for instanciado esse parametro não deve ser passado


server_default=func.now() diz que, quando a classe for instanciada, o resultado de func.now() será o valor atribuído a esse atributo. 
No caso, a data e hora em que ele foi instanciado
'''


table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(init=False, primary_key = True) 
    username:Mapped[str] = mapped_column(unique = True)
    password:Mapped[str]
    email:Mapped[str] = mapped_column(unique = True)
    created_at:Mapped[datetime] = mapped_column(init = False,server_default = func.now()
                                                )

@table_registry.mapped_as_dataclass
class Wine:
    __tablename__ = 'wines'
    id:Mapped[int] = mapped_column(init=False, primary_key = True) 
    name:Mapped[str] 
    wine_type:Mapped[str]
    price:Mapped[float]
    created_at:Mapped[datetime] = mapped_column(init = False,server_default = func.now())