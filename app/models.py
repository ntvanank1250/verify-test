from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app import database

Base = database.Base


class Server(Base):
    __tablename__ = "server"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String)
    description = Column(String)

class Domain(Base):
    __tablename__ = "domain"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    domain = Column(String)
