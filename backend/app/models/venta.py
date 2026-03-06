from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    medio_pago = Column(String(50), nullable=False)  # EFECTIVO, DEBITO, etc.
    estado = Column(String(20), default="COMPLETADA")  # COMPLETADA, ANULADA

    usuario = relationship("Usuario", backref="ventas")
    detalle = relationship("VentaDetalle", back_populates="venta", cascade="all, delete-orphan")


class VentaDetalle(Base):
    __tablename__ = "ventas_detalle"

    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    venta = relationship("Venta", back_populates="detalle")
    producto = relationship("Producto", backref="ventas_detalle")
