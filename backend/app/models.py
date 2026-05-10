from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(String(100))
    email = Column(
        String(100),
        unique=True
    )
    telefone = Column(String(20))
    morada = Column(String(200))
    nif = Column(String(20))