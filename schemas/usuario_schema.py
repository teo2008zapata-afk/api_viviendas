from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Esquema para registrar o actualizar una persona
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


# Esquema para devolver una persona
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)