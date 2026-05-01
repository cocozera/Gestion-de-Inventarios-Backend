from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import engine, Base
from app.api.routers import auth, productos, ventas

app = FastAPI(title="StockRL API", version="1.0.0")
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:1420", "http://127.0.0.1:1420"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(productos.router, prefix="/api")
app.include_router(ventas.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}


def init_db():
    """Crea todas las tablas en PostgreSQL. Ejecutar una vez al iniciar."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
