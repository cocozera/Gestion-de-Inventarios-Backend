from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    tipo_movimiento = Column(String(20), nullable=False)  # VENTA, INGRESO_PROVEEDOR, AJUSTE_MANUAL, MERMA
    cantidad = Column(Integer, nullable=False)  # Positiva o negativa
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
