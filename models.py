from sqlalchemy import Column, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DiaryEntry(Base):
    __tablename__ = 'entries'

    date = Column(Date, primary_key=True)
    content = Column(String)
