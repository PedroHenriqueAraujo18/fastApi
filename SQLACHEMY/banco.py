from sqlalchemy import create_engine

engine = create_engine(#Padrão de arquitetura conhecido como Factory
    'postgresql+psycopg://...'
)

print(f"{engine}")
print(engine.dialect)