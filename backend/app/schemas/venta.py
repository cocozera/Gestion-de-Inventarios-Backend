from pydantic import BaseModel
from decimal import Decimal
from typing import List
from datetime import datetime


class VentaItem(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal


class VentaCreate(BaseModel):
    """Payload desde React al cerrar venta"""
    usuario_id: int
    medio_pago: str  # EFECTIVO, DEBITO, BILLETERA_VIRTUAL
    total: Decimal
    items: List[VentaItem]


class VentaDetalleResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class VentaResponse(BaseModel):
    mensaje: str
    ticket_id: int


class VentaListResponse(BaseModel):
    id: int
    fecha_hora: datetime
    total: Decimal
    medio_pago: str
    estado: str

    class Config:
        from_attributes = True
