from src.Clase import Clase
from src.Escuelas import Escuelas
from src.Grupos import Grupos
from src.Anotacion import Anotacion
from src.modelos import ClaseData, EscuelaData, AnotacionData
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Instancia global de Escuelas
escuelas_instance = Escuelas()

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
def crear_clase(clase_data: ClaseData):
    """Crea una nueva clase y retorna el ID asignado."""
    try:
        nueva_clase = Clase(
            fecha=clase_data.fecha,
            depto=clase_data.depto,
            escuela=clase_data.escuela,
            grado=clase_data.grado,
            letra=clase_data.letra,
            nombreMaestra=clase_data.nombreMaestra,
        )
        clase_id = Clase.registrar(nueva_clase)
        return {
            "mensaje": "¡Clase creada exitosamente!",
            "id": clase_id,
            "grado": f"{nueva_clase.grado}° {nueva_clase.letra}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clases")
def get_clases():
    """Retorna todas las clases como lista."""
    return {"clases": Clase.darClases()}


@app.get("/clases/por-mes")
def get_clases_por_mes():
    """Retorna las clases agrupadas por mes, ordenadas cronológicamente."""
    return {"meses": Clase.darClasesPorMes()}


@app.get("/clases/{clase_id}")
def get_clase(clase_id: int):
    """Retorna una clase por su ID."""
    clase = Clase.buscarPorId(clase_id)
    if clase is None:
        raise HTTPException(status_code=404, detail=f"Clase con id {clase_id} no encontrada")
    anotacion_dict = None
    if clase.anotacion:
        anotacion_dict = {
            "dictada": clase.anotacion.dictada,
            "registroDeClase": clase.anotacion.RegistroDeClase,
            "correspondePago": clase.anotacion.correspondePago,
            "observaciones": clase.anotacion.observaciones,
        }
    return {
        "id": clase_id,
        "fecha": clase.fecha,
        "depto": clase.depto,
        "escuela": clase.escuela,
        "grado": clase.grado,
        "letra": clase.letra,
        "nombreMaestra": clase.nombreMaestra,
        "anotacion": anotacion_dict,
    }


# ── Anotaciones ─────────────────────────────────────────────────────────────

@app.post("/clases/{clase_id}/anotacion")
def agregar_anotacion(clase_id: int, datos: AnotacionData):
    """Crea y asocia una nueva Anotación a la clase indicada."""
    clase = Clase.buscarPorId(clase_id)
    if clase is None:
        raise HTTPException(status_code=404, detail=f"Clase con id {clase_id} no encontrada")

    nueva_anotacion = Anotacion(
        dictada=datos.dictada,
        RegistroDeClase=datos.registroDeClase,
        correspondePago=datos.correspondePago,
    )
    if datos.observaciones:
        nueva_anotacion.agregar_observaciones(datos.observaciones)

    clase.modificarAnotacion(nueva_anotacion)
    return {
        "mensaje": "Anotación agregada correctamente",
        "clase_id": clase_id,
        "anotacion": {
            "dictada": nueva_anotacion.dictada,
            "registroDeClase": nueva_anotacion.RegistroDeClase,
            "correspondePago": nueva_anotacion.correspondePago,
            "observaciones": nueva_anotacion.observaciones,
        },
    }


@app.put("/clases/{clase_id}/anotacion")
def actualizar_anotacion(clase_id: int, datos: AnotacionData):
    """Reemplaza la anotación de una clase existente."""
    clase = Clase.buscarPorId(clase_id)
    if clase is None:
        raise HTTPException(status_code=404, detail=f"Clase con id {clase_id} no encontrada")

    anotacion = Anotacion(
        dictada=datos.dictada,
        RegistroDeClase=datos.registroDeClase,
        correspondePago=datos.correspondePago,
    )
    if datos.observaciones:
        anotacion.agregar_observaciones(datos.observaciones)

    clase.modificarAnotacion(anotacion)
    return {
        "mensaje": "Anotación actualizada correctamente",
        "clase_id": clase_id,
    }


# ── Escuelas ─────────────────────────────────────────────────────────────────

@app.get("/escuelas")
def get_escuelas():
    return {"escuelas": escuelas_instance.darEscuelas()}


@app.post("/escuelas")
def agregar_escuela(escuela_data: EscuelaData):
    try:
        nombre = escuela_data.nombre.strip()
        if not nombre:
            raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")
        if nombre in escuelas_instance.darEscuelas():
            raise HTTPException(status_code=409, detail=f"La escuela '{nombre}' ya existe")
        escuelas_instance.agregar_escuela(nombre)
        return {"mensaje": f"Escuela '{nombre}' agregada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/escuelas")
def eliminar_escuela(escuela_data: EscuelaData):
    try:
        nombre = escuela_data.nombre.strip()
        if nombre not in escuelas_instance.darEscuelas():
            raise HTTPException(status_code=404, detail=f"La escuela '{nombre}' no existe")
        escuelas_instance.eliminar_escuela(nombre)
        return {"mensaje": f"Escuela '{nombre}' eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Grupos ───────────────────────────────────────────────────────────────────

@app.get("/grupos")
def get_grupos():
    return {"grupos": Grupos().darGrupos()}


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
