from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=True)
    rol = Column(String(20), nullable=False)  # CAJERO, REPOSITOR, ADMIN
