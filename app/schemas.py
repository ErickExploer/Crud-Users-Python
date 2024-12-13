# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List

class UserSchema(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dni: Optional[str] = None  # DNI como cadena
    age: Optional[int] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True  # Permite la conversión de objetos SQLAlchemy
        from_attributes = True  # Habilita 'from_orm' para trabajar con los atributos de los objetos SQLAlchemy

class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)

class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[List[dict]] = []  # 'result' es opcional