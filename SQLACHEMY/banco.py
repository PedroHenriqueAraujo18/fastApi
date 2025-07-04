from sqlalchemy import create_engine

engine_pg = create_engine(#Padrão de arquitetura conhecido como Factory
    'postgresql+psycopg://...',
    echo=True
)

engine_sql = create_engine(
    'sqlite://',
    echo=True
)

pg_con = engine_pg.connect()
sqlite_con = engine_sql.connect()

print(pg_con.connection.dbapi_connection)
pg_con.close()
sqlite_con.close()
