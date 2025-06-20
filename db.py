import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_PATH = "diary.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Session = sessionmaker(bind=engine)


def initialize_database():
    if not os.path.exists(DB_PATH):
        print("Создаю базу данных...")
        Base.metadata.create_all(engine)
