from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user, require_roles
from app.models import Producto, Usuario
from app.schemas import ProductoBusqueda, ProductoResponse, ProductoCreate, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/buscar/{codigo_barras}", response_model=ProductoBusqueda)
def buscar_por_codigo(
    codigo_barras: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    producto = (
        db.query(Producto)
        .filter(
            Producto.codigo_barras == codigo_barras.strip(),
            Producto.estado == True,
        )
        .first()
    )
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado o inactivo")
    return producto


@router.get("/", response_model=List[ProductoResponse])
def listar_productos(
    q: Optional[str] = Query(None, description="Buscar por nombre o código"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("ADMIN", "REPOSITOR", "CAJERO")),
):
    query = db.query(Producto)
    if q:
        query = query.filter(
            (Producto.nombre.ilike(f"%{q}%")) | (Producto.codigo_barras.ilike(f"%{q}%"))
        )
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=ProductoResponse)
def crear_producto(
    data: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("ADMIN", "REPOSITOR")),
):
    if db.query(Producto).filter(Producto.codigo_barras == data.codigo_barras).first():
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese código de barras")
    producto = Producto(**data.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    data: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("ADMIN", "REPOSITOR")),
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(producto, k, v)
    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("ADMIN")),
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.estado = False  # Soft delete
    db.commit()
    return None
