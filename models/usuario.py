from sqlalchemy import Column, Integer, String

from database.database import Base


class User(Base):
    # Nombre de la tabla
    __tablename__ = "usuarios"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(100), nullable=False)