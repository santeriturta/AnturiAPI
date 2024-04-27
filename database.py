from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float, Boolean
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./sensor.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = sqlalchemy.orm.declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
