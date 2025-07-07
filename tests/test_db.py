from sqlalchemy import select

from fast_zero.models import User #Wine

'''
O método .add da sessão, adiciona o registro a sessão.
O dado fica em um estado transiente. 
Ele não foi adicionado ao banco de dados ainda. 
Mas já está reservado na sessão. 
Ele é uma aplicação do padrão de projeto Unidade de trabalho.
============================================================
No momento em que existem dados transientes na sessão e 
queremos "performar" efetivamente as ações no banco de dados. 
Usamos o método .commit.
============================================================

'''

def teste_create_user_in_db(session):
    new_user = User(username ='pedro',password='secret',email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'pedro'))
    
    assert user.username == 'pedro'