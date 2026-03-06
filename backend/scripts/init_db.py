"""
Script para crear las tablas en PostgreSQL y opcionalmente un usuario admin inicial.
Ejecutar desde la raíz del backend: python -m scripts.init_db
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base, SessionLocal
from app.models import Categoria, Producto, Usuario, Venta, VentaDetalle, MovimientoStock
from app.core.auth import get_password_hash


def main():
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")

    db = SessionLocal()
    try:
        if db.query(Usuario).filter(Usuario.username == "admin").first():
            print("Usuario admin ya existe.")
            return
        admin = Usuario(
            username="admin",
            password_hash=get_password_hash("admin123"),
            nombre="Administrador",
            rol="ADMIN",
        )
        db.add(admin)
        cajero = Usuario(
            username="cajero",
            password_hash=get_password_hash("cajero123"),
            nombre="Cajero Demo",
            rol="CAJERO",
        )
        db.add(cajero)
        cat = Categoria(nombre="General", descripcion="Productos varios")
        db.add(cat)
        db.commit()
        db.refresh(cat)
        p = Producto(
            codigo_barras="779000000001",
            nombre="Producto Demo",
            categoria_id=cat.id,
            precio_venta=100.50,
            stock_actual=50,
            stock_minimo=5,
        )
        db.add(p)
        db.commit()
        print("Usuario admin (admin / admin123) y cajero (cajero / cajero123) creados.")
        print("Producto demo 779000000001 creado.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
