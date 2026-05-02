from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.auth import require_roles
from app.models import Usuario, Venta
from app.schemas import VentaCreate, VentaResponse, VentaListResponse
from app.services.venta_service import procesar_venta

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.get("/", response_model=List[VentaListResponse])
def listar_ventas(
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("ADMIN")),
):
    query = db.query(Venta).order_by(Venta.fecha_hora.desc())
    if desde:
        query = query.filter(Venta.fecha_hora >= desde)
    if hasta:
        query = query.filter(Venta.fecha_hora <= hasta)
    return query.limit(limit).all()


@router.post("/", response_model=VentaResponse)
def crear_venta(
    payload: VentaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("ADMIN", "CAJERO")),
):
    if payload.usuario_id != current_user.id and current_user.rol != "ADMIN":
        raise HTTPException(status_code=403, detail="Solo puede registrar ventas con su propio usuario")
    ticket_id = procesar_venta(db, payload)
    return VentaResponse(mensaje="Venta procesada correctamente", ticket_id=ticket_id)
