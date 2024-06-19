from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Banco(Base):
    __tablename__ = "banco"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement="auto",
        index=True,
        nullable=False
    )
    
    name = Column(
        String(50),
        nullable=False,
        unique=True,
    )


class Tasa(Base):
    __tablename__ = "tasa"
    
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=False
    )
    
    usd_compra = Column(
        Numeric(10, 2, asdecimal=True,),
        nullable=True,
    )
    usd_venta = Column(
        Numeric(10, 2, asdecimal=True,),
        nullable=True,
    )
    
    fecha = Column(
        Date,
        nullable=False, 
        
    )
    
    banco = Column(
        ForeignKey("banco.id"),
        nullable=True,
    )
    

def db_connect(database_url:str):
    return create_engine(database_url)

def create_table(engine):
    Base.metadata.create_all(engine)