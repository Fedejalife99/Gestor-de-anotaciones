from pydantic import BaseModel
from typing import Optional


class ClaseData(BaseModel):
    """Modelo Pydantic para recibir datos de Clase."""
    fecha: str                        # ej: "2026-03-29"
    depto: str
    escuela: str
    grado: int
    letra: str                        # A, B, C, D, E
    nombreMaestra: Optional[str] = None


class EscuelaData(BaseModel):
    """Modelo Pydantic para recibir datos de Escuela."""
    nombre: str


class AnotacionData(BaseModel):
    """Modelo Pydantic para crear o actualizar una Anotación."""
    dictada: bool
    registroDeClase: str
    correspondePago: bool
    observaciones: Optional[str] = None
