from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class ProductoBusqueda(BaseModel):
    id: int
    nombre: str
    precio_venta: float
    stock_actual: int

    class Config:
        from_attributes = True


class ProductoResponse(BaseModel):
    id: int
    codigo_barras: str
    nombre: str
    categoria_id: Optional[int] = None
    precio_costo: float
    precio_venta: float
    stock_actual: int
    stock_minimo: int
    estado: bool

    class Config:
        from_attributes = True


class ProductoCreate(BaseModel):
    codigo_barras: str
    nombre: str
    categoria_id: Optional[int] = None
    precio_costo: Decimal = Decimal("0")
    precio_venta: Decimal
    stock_actual: int = 0
    stock_minimo: int = 0
    estado: bool = True


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria_id: Optional[int] = None
    precio_costo: Optional[Decimal] = None
    precio_venta: Optional[Decimal] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None
    estado: Optional[bool] = None
