from pydantic import BaseModel, ConfigDict, Field


# Esquema para registrar o actualizar una vivienda
class dwellingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    neighborhood: str = Field(min_length=2, max_length=100)
    structure: str = Field(min_length=2, max_length=100)
    floors: int = Field(gt=0)


# Esquema para devolver una vivienda
class dwellingResponse(BaseModel):
    id: int
    name: str
    neighborhood: str
    structure: str
    floors: int

    model_config = ConfigDict(from_attributes=True)