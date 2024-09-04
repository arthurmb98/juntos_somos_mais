from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///mydatabase.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def check_tables():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        print("Tables in database:", [table[0] for table in tables])


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")
    check_tables()

