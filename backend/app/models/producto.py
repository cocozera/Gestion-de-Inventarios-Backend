from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_barras = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(150), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    precio_costo = Column(Numeric(10, 2), default=0)
    precio_venta = Column(Numeric(10, 2), nullable=False)
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=0)
    estado = Column(Boolean, default=True)

    categoria = relationship("Categoria", backref="productos")
