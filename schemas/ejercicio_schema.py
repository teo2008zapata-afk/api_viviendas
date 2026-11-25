from pydantic import BaseModel, ConfigDict, Field


# Esquema para registrar o actualizar una vivienda
class dwellingCreate(BaseModel):
    code: str = Field(min_length=2, max_length=100)
    address: str = Field(min_length=2, max_length=100)
    neighborhood: str = Field(min_length=2, max_length=100)
    rooms: int = Field(gt=0)
    area: int = Field(gt=0)


# Esquema para devolver una vivienda
class dwellingResponse(BaseModel):
    id: int
    code: str
    address: str
    neighborhood: str
    rooms: int
    area: int

    model_config = ConfigDict(from_attributes=True)