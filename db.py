# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base  

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./test.db"  # ou a URL do banco de dados que você está utilizando
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação das tabelas no banco de dados
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()  # Chame a função para criar as tabelas se este for o módulo principal
