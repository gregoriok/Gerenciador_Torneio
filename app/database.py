from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@localhost/futebol_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

MONGO_DETAILS = "mongodb://root:root@localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
mongodb = client.futebol_live