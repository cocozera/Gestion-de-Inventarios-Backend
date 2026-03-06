from pydantic import BaseModel
from typing import Optional


class UsuarioCreate(BaseModel):
    username: str
    password: str
    nombre: Optional[str] = None
    rol: str  # CAJERO, REPOSITOR, ADMIN


class UsuarioResponse(BaseModel):
    id: int
    username: str
    nombre: Optional[str] = None
    rol: str

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
