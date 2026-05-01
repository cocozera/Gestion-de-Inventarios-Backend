from pydantic import BaseModel
from decimal import Decimal
from typing import List
from datetime import datetime


class VentaItem(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal


class VentaCreate(BaseModel):
    usuario_id: int
    medio_pago: str
    total: Decimal
    items: List[VentaItem]


class VentaResponse(BaseModel):
    mensaje: str
    ticket_id: int


class VentaListResponse(BaseModel):
    id: int
    fecha_hora: datetime
    total: float
    medio_pago: str
    estado: str

    class Config:
        from_attributes = True
