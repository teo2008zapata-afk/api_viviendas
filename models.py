from sqlalchemy import Column, Integer, String
from database import Base

class dwelling(Base):
    # Nombre de la tabla
    __tablename__ = "viviendas"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False)
    address = Column(String(100), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    rooms = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)