import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. Carrega variáveis de ambiente (útil para rodar local fora do Docker)
load_dotenv()

# 2. Pega o endereço do banco definido no docker-compose ou .env
# Exemplo: postgresql+psycopg2://user:pass@db:5432/pulso_db
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não está definida!")

# 3. Cria o ENGINE (O Motor)
# É ele que gerencia o pool de conexões com o PostgreSQL
engine = create_engine(DATABASE_URL)

# 4. Cria a SESSIONLOCAL (A Fábrica de Sessões)
# Cada requisição do usuário vai ganhar uma "sessão" temporária para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Cria a BASE (O Molde)
# Todas as suas tabelas (Users, Messages) vão herdar desta classe
Base = declarative_base()

# 6. Dependência (Para usar no FastAPI)
# Essa função garante que o banco abre e FECHA a conexão a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()