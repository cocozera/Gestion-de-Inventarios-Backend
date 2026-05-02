# Backend — StockAI Pollería

API REST construida con **FastAPI + SQLAlchemy**. Base de datos en **Supabase (PostgreSQL)** — no hay nada que instalar localmente para la DB, ya está en la nube.

---

## Requisitos previos (instalar en Windows)

- **Python 3.11** → https://www.python.org/downloads/ (marcar "Add to PATH" durante la instalación)
- **Git** (opcional, solo si se clona el repo)

---

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py               # Punto de entrada, CORS, routers
│   ├── core/
│   │   ├── auth.py           # JWT, hash de contraseñas, dependencias de autenticación
│   │   ├── config.py         # Variables de entorno (lee el .env)
│   │   └── database.py       # Conexión SQLAlchemy a Supabase
│   ├── models/               # Tablas de la BD (SQLAlchemy ORM)
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   ├── venta.py
│   │   ├── categoria.py
│   │   └── movimiento_stock.py
│   ├── schemas/              # Validación de entrada/salida (Pydantic)
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   └── venta.py
│   ├── api/routers/          # Endpoints HTTP
│   │   ├── auth.py           # POST /api/auth/login, /register, GET /me
│   │   ├── productos.py      # CRUD productos + búsqueda por código de barras
│   │   └── ventas.py         # GET /api/ventas, POST /api/ventas
│   └── services/
│       └── venta_service.py  # Lógica transaccional: descuenta stock, registra movimientos
├── .env                      # Variables de entorno (NO subir a git)
├── .env.example              # Plantilla del .env
└── requirements.txt
```

---

## Pasos para correr el backend

### 1. Abrir terminal en la carpeta del backend

```
cd "Gestion de Inventarios - Polleria\Gestion-de-Inventarios-Backend\backend"
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual (Windows)

```bash
.venv\Scripts\activate
```

> El prompt debe mostrar `(.venv)` al inicio.

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Verificar el archivo .env

El archivo `.env` debe existir en la raíz del backend con este contenido:

```
DATABASE_URL=postgresql://postgres.ibkoofulzdcbclbmaplq:Ramiro45806009@aws-1-us-east-1.pooler.supabase.com:6543/postgres
SECRET_KEY=cambiar-en-produccion-secret-key-muy-segura
```

> La base de datos es Supabase (nube). No hace falta instalar PostgreSQL local.

### 6. Levantar el servidor

```bash
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

El backend queda corriendo en: **http://localhost:8000**

Documentación interactiva disponible en: **http://localhost:8000/docs**

---

## Endpoints principales

| Método | Ruta | Descripción | Rol requerido |
|--------|------|-------------|---------------|
| POST | `/api/auth/login` | Login, devuelve JWT | — |
| GET | `/api/productos/` | Listar productos | ADMIN, CAJERO, REPOSITOR |
| GET | `/api/productos/buscar/{codigo}` | Buscar por código de barras | Autenticado |
| POST | `/api/productos/` | Crear producto | ADMIN, REPOSITOR |
| PUT | `/api/productos/{id}` | Editar producto | ADMIN, REPOSITOR |
| GET | `/api/ventas/` | Historial de ventas | ADMIN |
| POST | `/api/ventas/` | Registrar venta | ADMIN, CAJERO |

---

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | ADMIN |
| cajero | cajero123 | CAJERO |

---

## Notas importantes

- El backend escucha en el puerto **8000**. El frontend espera que esté en `http://localhost:8000`.
- Los tokens JWT duran **8 horas**.
- Cada venta descuenta stock automáticamente y registra un movimiento en `movimientos_stock`.
- El `DELETE` de producto es un **soft delete** (cambia `estado = false`, no borra el registro).
