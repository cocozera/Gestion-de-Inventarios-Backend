from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_password_hash, create_access_token, get_current_user, verify_password
from app.models import Usuario
from app.schemas import UsuarioLogin, UsuarioCreate, UsuarioResponse, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = create_access_token(data={"sub": str(user.id)})
    return Token(
        access_token=token,
        usuario=UsuarioResponse.model_validate(user),
    )


@router.post("/register", response_model=UsuarioResponse)
def register(data: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.username == data.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    user = Usuario(
        username=data.username,
        password_hash=get_password_hash(data.password),
        nombre=data.nombre,
        rol=data.rol,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user
