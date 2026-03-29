from src.modelos import ClaseData, EscuelaData, AnotacionData
from src.gestorBD import (
    crear_tablas, SessionLocal, ClaseDB, EscuelaDB, AnotacionDB, GrupoDB
)
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from collections import defaultdict
import uvicorn

app = FastAPI()

# Crear tablas al iniciar
crear_tablas()

# ── Dependencia para obtener sesión de BD ────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── Rutas de páginas ────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/static/index.html")
async def serve_index():
    return FileResponse("static/index.html")


# ── Clases ──────────────────────────────────────────────────────────────────
@app.post("/clases")
def crear_clase(clase_data: ClaseData, db: Session = Depends(get_db)):
    """Crea una nueva clase y retorna el ID asignado."""
    try:
        # Verificar que la escuela existe
        escuela = db.query(EscuelaDB).filter(EscuelaDB.nombre == clase_data.escuela).first()
        if not escuela:
            raise HTTPException(status_code=404, detail=f"La escuela '{clase_data.escuela}' no existe")
        
        # Crear nueva clase
        nueva_clase = ClaseDB(
            fecha=clase_data.fecha,
            depto=clase_data.depto,
            escuela=clase_data.escuela,
            grado=clase_data.grado,
            letra=clase_data.letra,
            nombreMaestra=clase_data.nombreMaestra,
        )
        
        db.add(nueva_clase)
        db.commit()
        db.refresh(nueva_clase)
        
        return {
            "mensaje": "¡Clase creada exitosamente!",
            "id": nueva_clase.id,
            "grado": f"{nueva_clase.grado}° {nueva_clase.letra}",
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clases")
def get_clases(db: Session = Depends(get_db)):
    """Retorna todas las clases como lista."""
    clases = db.query(ClaseDB).all()
    return {"clases": [c.to_dict() for c in clases]}


@app.get("/clases/por-mes")
def get_clases_por_mes(db: Session = Depends(get_db)):
    """Retorna las clases agrupadas por mes."""
    clases = db.query(ClaseDB).all()
    meses = defaultdict(list)
    
    MESES = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    for clase in clases:
        try:
            from datetime import datetime as dt
            fecha_dt = dt.strptime(clase.fecha, "%Y-%m-%d")
            mes_nombre = f"{MESES[fecha_dt.month - 1]} {fecha_dt.year}"
            meses[mes_nombre].append(clase.to_dict())
        except Exception:
            meses["Sin clasificar"].append(clase.to_dict())
    
    # Ordenar cronológicamente: generar todas las keys "Mes YYYY" y ordenarlas por (año, mes)
    def sort_key(k):
        try:
            partes = k.split()
            return (int(partes[1]), MESES.index(partes[0]))
        except Exception:
            return (9999, 99)

    meses_ordenados = dict(sorted(meses.items(), key=lambda kv: sort_key(kv[0])))
    
    return {"meses": meses_ordenados}


@app.get("/clases/{clase_id}")
def get_clase(clase_id: int, db: Session = Depends(get_db)):
    """Retorna una clase por su ID."""
    clase = db.query(ClaseDB).filter(ClaseDB.id == clase_id).first()
    if clase is None:
        raise HTTPException(status_code=404, detail=f"Clase con id {clase_id} no encontrada")
    
    return clase.to_dict()


@app.delete("/clases/{clase_id}")
def eliminar_clase(clase_id: int, db: Session = Depends(get_db)):
    """Elimina una clase por su ID."""
    clase = db.query(ClaseDB).filter(ClaseDB.id == clase_id).first()
    if clase is None:
        raise HTTPException(status_code=404, detail=f"Clase con id {clase_id} no encontrada")
    
    db.delete(clase)
    db.commit()
    return {"mensaje": f"Clase {clase_id} eliminada correctamente"}


# ── Anotaciones ─────────────────────────────────────────────────────────────

@app.post("/clases/{clase_id}/anotacion")
def agregar_anotacion(clase_id: int, datos: AnotacionData, db: Session = Depends(get_db)):
    """Crea y asocia una nueva anotación a la clase indicada."""
    clase = db.query(ClaseDB).filter(ClaseDB.id == clase_id).first()
    if clase is None:
        raise HTTPException(status_code=404, detail=f"Clase con id {clase_id} no encontrada")
    
    try:
        anotacion = db.query(AnotacionDB).filter(AnotacionDB.id == clase.anotacion).first()
        # Actualizar campos de anotación
        if anotacion:
            anotacion.dictada = datos.dictada
            anotacion.registroClase = datos.registroDeClase
            anotacion.correspondePago = datos.correspondePago
            anotacion.Observaciones = datos.observaciones
            db.commit()
            db.refresh(anotacion)
        else:
            nueva_anotacion = AnotacionDB(
                dictada=datos.dictada,
                registroClase=datos.registroDeClase,
                correspondePago=datos.correspondePago,
                observaciones=datos.observaciones
            )
            db.add(nueva_anotacion)
            db.commit()
            db.refresh(nueva_anotacion)
            
            clase.anotacion = nueva_anotacion.id
        db.commit()
        db.refresh(clase)
        
        return {
            "mensaje": "Anotación agregada correctamente",
            "clase_id": clase_id,
            "anotacion": clase.to_dict()["anotacion"],
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/clases/{clase_id}/anotacion")
def actualizar_anotacion(clase_id: int, datos: AnotacionData, db: Session = Depends(get_db)):
    """Actualiza la anotación de una clase existente."""
    clase = db.query(ClaseDB).filter(ClaseDB.id == clase_id).first()
    if clase is None:
        raise HTTPException(status_code=404, detail=f"Clase con id {clase_id} no encontrada")

    anotacion = db.query(AnotacionDB).filter(AnotacionDB.id == clase.anotacion).first()
    if anotacion is None:
        raise HTTPException(status_code=404, detail=f"La clase {clase_id} no tiene anotación aún. Usá POST para crear una.")

    try:
        anotacion.dictada = datos.dictada
        anotacion.registroClase = datos.registroDeClase
        anotacion.correspondePago = datos.correspondePago
        anotacion.observaciones = datos.observaciones

        db.commit()
        db.refresh(anotacion)

        return {
            "mensaje": "Anotación actualizada correctamente",
            "clase_id": clase_id,
            "anotacion": anotacion.to_dict(),
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── Escuelas ────────────────────────────────────────────────────────────────

@app.get("/escuelas")
def get_escuelas(db: Session = Depends(get_db)):
    """Retorna todas las escuelas."""
    escuelas = db.query(EscuelaDB).all()
    return {"escuelas": [e.nombre for e in escuelas]}


@app.post("/escuelas")
def agregar_escuela(escuela_data: EscuelaData, db: Session = Depends(get_db)):
    """Agrega una nueva escuela."""
    try:
        nombre = escuela_data.nombre.strip()
        if not nombre:
            raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")
        
        # Verificar si ya existe
        existente = db.query(EscuelaDB).filter(EscuelaDB.nombre == nombre).first()
        if existente:
            raise HTTPException(status_code=409, detail=f"La escuela '{nombre}' ya existe")
        
        nueva_escuela = EscuelaDB(nombre=nombre)
        db.add(nueva_escuela)
        db.commit()
        
        return {"mensaje": f"Escuela '{nombre}' agregada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/escuelas")
def eliminar_escuela(escuela_data: EscuelaData, db: Session = Depends(get_db)):
    """Elimina una escuela solo si no tiene clases asociadas."""
    try:
        nombre = escuela_data.nombre.strip()
        escuela = db.query(EscuelaDB).filter(EscuelaDB.nombre == nombre).first()

        if not escuela:
            raise HTTPException(status_code=404, detail=f"La escuela '{nombre}' no existe")

        clases_asociadas = db.query(ClaseDB).filter(ClaseDB.escuela == nombre).count()
        if clases_asociadas > 0:
            raise HTTPException(
                status_code=409,
                detail=f"No se puede eliminar '{nombre}': tiene {clases_asociadas} clase(s) asociada(s)"
            )

        db.delete(escuela)
        db.commit()

        return {"mensaje": f"Escuela '{nombre}' eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── Grupos ───────────────────────────────────────────────────────────────────

@app.get("/grupos")
def get_grupos(db: Session = Depends(get_db)):
    """Retorna todos los grupos."""
    grupos = db.query(GrupoDB).all()
    return {"grupos": [g.to_dict() for g in grupos]}


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
