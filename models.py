from sqlalchemy import Column, Integer, String
from database import Base

class dwelling(Base):
    # Nombre de la tabla
    __tablename__ = "viviendas"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    structure = Column(String(100), nullable=False)
    floors = Column(Integer, nullable=False)