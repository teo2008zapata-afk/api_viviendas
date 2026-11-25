import base64
import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.usuario import User
from schemas.usuario_schema import UserCreate, UserResponse

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    iterations = 260_000
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    salt_text = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
    digest_text = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return f"pbkdf2_sha256${iterations}${salt_text}${digest_text}"


@router.get("", response_model=list[UserResponse])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("", response_model=UserResponse, status_code=201)
def create_usuario(data: UserCreate, db: Session = Depends(get_db)):
    usuario = User(
        name=data.name,
        email=data.email,
        password=_hash_password(data.password),
    )
    db.add(usuario)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario con ese correo",
        )

    db.refresh(usuario)
    return usuario


@router.put("/{user_id}", response_model=UserResponse)
def update_usuario(
    user_id: int,
    data: UserCreate,
    db: Session = Depends(get_db),
):
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.name = data.name
    usuario.email = data.email
    usuario.password = _hash_password(data.password)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario con ese correo",
        )

    db.refresh(usuario)
    return usuario


@router.delete("/{user_id}")
def delete_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}
