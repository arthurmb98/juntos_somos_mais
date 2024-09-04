from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Defina a URL de conexão para o seu banco de dados
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Crie o engine SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Crie uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
