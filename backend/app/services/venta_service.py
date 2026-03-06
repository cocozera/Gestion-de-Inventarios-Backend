"""
Lógica transaccional de ventas: crea venta, detalle, actualiza stock y registra movimientos.
Si algo falla (ej. stock negativo), hace ROLLBACK y devuelve error.
"""
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Venta, VentaDetalle, Producto, MovimientoStock
from app.schemas import VentaCreate, VentaItem


def procesar_venta(db: Session, payload: VentaCreate) -> int:
    try:
        # 1. Crear cabecera de venta
        venta = Venta(
            usuario_id=payload.usuario_id,
            total=payload.total,
            medio_pago=payload.medio_pago,
            estado="COMPLETADA",
        )
        db.add(venta)
        db.flush()  # Para obtener venta.id sin commit

        for item in payload.items:
            # 2. Verificar stock y bloquear fila
            producto = db.query(Producto).filter(
                Producto.id == item.producto_id,
                Producto.estado == True,
            ).with_for_update().first()

            if not producto:
                raise HTTPException(
                    status_code=400,
                    detail=f"Producto id {item.producto_id} no existe o está inactivo",
                )
            if producto.stock_actual < item.cantidad:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock_actual}",
                )

            subtotal = Decimal(str(item.precio_unitario)) * item.cantidad

            # 3. Insertar detalle
            detalle = VentaDetalle(
                venta_id=venta.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=subtotal,
            )
            db.add(detalle)

            # 4. Descontar stock
            producto.stock_actual -= item.cantidad

            # 5. Registrar movimiento de auditoría
            mov = MovimientoStock(
                producto_id=producto.id,
                usuario_id=payload.usuario_id,
                tipo_movimiento="VENTA",
                cantidad=-item.cantidad,
            )
            db.add(mov)

        db.commit()
        db.refresh(venta)
        return venta.id
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar la venta: {str(e)}")
