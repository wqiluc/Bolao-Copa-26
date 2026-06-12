import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_BANCO = os.environ.get("DATABASE_URL", "postgresql://bolao:bolao123@localhost:5432/bolao_copa26")

engine = create_engine(URL_BANCO)
SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def obter_bd():
    bd = SessaoLocal()
    
    try:
        yield bd
    finally:
        bd.close()