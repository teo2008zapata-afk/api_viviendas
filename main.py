from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import dwelling
from schemas import dwellingCreate, dwellingResponse

# Crear la tabla en Neon si todavía no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Viviendas API")


# ====================================
# GET: Consultar todas las viviendas
# ====================================
@app.get("/viviendas", response_model=list[dwellingResponse])
def get_viviendas(db: Session = Depends(get_db)):
    viviendas = db.query(dwelling).all()
    return viviendas


# ====================================
# GET: Consultar viviendas por barrio
# ====================================
@app.get("/viviendas/barrio/{neighborhood}", response_model=list[dwellingResponse])
def get_viviendas_por_barrio(
    neighborhood: str,
    db: Session = Depends(get_db)
):
    viviendas = db.query(dwelling).filter(
        dwelling.neighborhood.ilike(neighborhood)
    ).all()
    return viviendas


# ====================================
# GET: Consultar una vivienda
# ====================================
@app.get("/viviendas/{Dwelling_id}", response_model=dwellingResponse)
def get_Dwelling(
    Dwelling_id: int,
    db: Session = Depends(get_db)
):
    Dwelling = db.query(dwelling).filter(
        dwelling.id == Dwelling_id
    ).first()

    if Dwelling is None:
        raise HTTPException(
            status_code=404,
            detail="dwelling not found"
        )

    return Dwelling


# ====================================
# POST: Registrar una vivienda
# ====================================
@app.post("/viviendas", response_model=dwellingResponse, status_code=201)
def create_Dwelling(
    data: dwellingCreate,
    db: Session = Depends(get_db)
):

    Dwelling = dwelling(
        code=data.code,
        address=data.address,
        neighborhood=data.neighborhood,
        rooms=data.rooms,
        area=data.area
    )

    db.add(Dwelling)
    db.commit()
    db.refresh(Dwelling)

    return Dwelling


# ====================================
# PUT: Actualizar una vivienda
# ====================================
@app.put("/viviendas/{Dwelling_id}", response_model=dwellingResponse)
def update_Dwelling(
    Dwelling_id: int,
    data: dwellingCreate,
    db: Session = Depends(get_db)
):
    Dwelling = db.query(dwelling).filter(
        dwelling.id == Dwelling_id
    ).first()

    if Dwelling is None:
        raise HTTPException(
            status_code=404,
            detail="dwelling not found"
        )

    Dwelling.code = data.code
    Dwelling.address = data.address
    Dwelling.neighborhood = data.neighborhood
    Dwelling.rooms = data.rooms
    Dwelling.area = data.area

    db.commit()
    db.refresh(Dwelling)

    return Dwelling


# ====================================
# DELETE: Eliminar una vivienda
# ====================================
@app.delete("/viviendas/{Dwelling_id}")
def delete_Dwelling(
    Dwelling_id: int,
    db: Session = Depends(get_db)
):
    Dwelling = db.query(dwelling).filter(
        dwelling.id == Dwelling_id
    ).first()

    if Dwelling is None:
        raise HTTPException(
            status_code=404,
            detail="dwelling not found"
        )

    db.delete(Dwelling)
    db.commit()

    return {
        "message": "dwelling deleted successfully"
    }