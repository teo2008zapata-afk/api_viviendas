from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from models.ejercicio import dwelling
from schemas.ejercicio_schema import dwellingCreate, dwellingResponse

router = APIRouter(prefix="/viviendas", tags=["viviendas"])


@router.get("", response_model=list[dwellingResponse])
def get_viviendas(db: Session = Depends(get_db)):
    return db.query(dwelling).all()


@router.get("/barrio/{neighborhood}", response_model=list[dwellingResponse])
def get_viviendas_por_barrio(
    neighborhood: str,
    db: Session = Depends(get_db),
):
    return db.query(dwelling).filter(
        dwelling.neighborhood.ilike(neighborhood)
    ).all()


@router.get("/{dwelling_id}", response_model=dwellingResponse)
def get_dwelling(dwelling_id: int, db: Session = Depends(get_db)):
    vivienda = db.query(dwelling).filter(dwelling.id == dwelling_id).first()
    if vivienda is None:
        raise HTTPException(status_code=404, detail="Vivienda no encontrada")
    return vivienda


@router.post("", response_model=dwellingResponse, status_code=201)
def create_dwelling(data: dwellingCreate, db: Session = Depends(get_db)):
    vivienda = dwelling(**data.model_dump())
    db.add(vivienda)
    db.commit()
    db.refresh(vivienda)
    return vivienda


@router.put("/{dwelling_id}", response_model=dwellingResponse)
def update_dwelling(
    dwelling_id: int,
    data: dwellingCreate,
    db: Session = Depends(get_db),
):
    vivienda = db.query(dwelling).filter(dwelling.id == dwelling_id).first()
    if vivienda is None:
        raise HTTPException(status_code=404, detail="Vivienda no encontrada")

    for field, value in data.model_dump().items():
        setattr(vivienda, field, value)

    db.commit()
    db.refresh(vivienda)
    return vivienda


@router.delete("/{dwelling_id}")
def delete_dwelling(dwelling_id: int, db: Session = Depends(get_db)):
    vivienda = db.query(dwelling).filter(dwelling.id == dwelling_id).first()
    if vivienda is None:
        raise HTTPException(status_code=404, detail="Vivienda no encontrada")

    db.delete(vivienda)
    db.commit()
    return {"message": "Vivienda eliminada correctamente"}
