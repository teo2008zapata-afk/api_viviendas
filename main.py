from fastapi import FastAPI

from database.database import Base, engine
from routers.usuarios import router as usuarios_router
from routers.viviendas import router as viviendas_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Viviendas y Usuarios")

app.include_router(viviendas_router)
app.include_router(usuarios_router)