# Gestor de Anotaciones

Sistema web para registrar y gestionar clases de maestras, desarrollado con **FastAPI** y **JavaScript vanilla**. Permite llevar un control de clases dictadas, sus anotaciones y el seguimiento de pagos correspondientes.

---

## Stack tecnológico

### Backend
- **FastAPI** — framework web moderno con validación automática y documentación integrada (`/docs`)
- **SQLAlchemy** — ORM para interacción con la base de datos mediante modelos de Python
- **SQLite** — base de datos embebida, sin necesidad de servidor externo
- **Pydantic v2** — validación y serialización de datos de entrada
- **Uvicorn** — servidor ASGI

### Frontend
- **HTML5 + CSS3 + JavaScript Vanilla** — sin frameworks ni dependencias externas
- Comunicación con el backend vía `fetch` API (XHR síncrono en pruebas)
- Diseño responsive con gradientes, backdrop blur y animaciones CSS

---

## Estructura del proyecto

```
Anotaciones/
│
├── main.py                  # Aplicación FastAPI y definición de endpoints
├── requirements.txt         # Dependencias del proyecto
├── README.md
├── .gitignore
│
├── src/
│   ├── gestorBD.py          # Modelos ORM (SQLAlchemy) y configuración de la BD
│   ├── modelos.py           # Modelos Pydantic para validación de requests
│   ├── Clase.py             # Clase de dominio (lógica de negocio)
│   ├── Anotacion.py         # Clase de dominio para anotaciones
│   ├── Escuelas.py          # Gestión de escuelas en memoria (legacy)
│   ├── Grupos.py            # Gestión de grupos
│   └── __init__.py
│
└── static/                  # Frontend (servido por FastAPI como archivos estáticos)
    ├── index.html           # Formulario para crear nueva clase
    ├── clases.html          # Vista de todas las clases con filtros y modal de detalle
    ├── anotacion.html       # Formulario para agregar/editar anotación a una clase
    └── escuelas.html        # ABM de escuelas
```

---

## Decisiones de diseño

### Persistencia: SQLite + SQLAlchemy
Se migró de un almacenamiento en memoria (diccionario de clase con `_clases_registradas`) a **SQLite con SQLAlchemy ORM**. La decisión fue pragmática: SQLite no requiere instalar ni configurar ningún servidor externo, el archivo `.db` vive junto al proyecto, y SQLAlchemy permite migrar a PostgreSQL o MySQL en el futuro cambiando solo el `DATABASE_URL`.

Las tablas se crean automáticamente al iniciar el servidor con `crear_tablas()`.

### Separación entre modelos ORM y modelos de dominio
Existen dos capas de modelos con responsabilidades distintas:
- **`src/gestorBD.py`** — modelos ORM (`ClaseDB`, `AnotacionDB`, `EscuelaDB`, `GrupoDB`) que mapean directamente a tablas SQL. Cada uno tiene un método `to_dict()` para serializar a JSON.
- **`src/modelos.py`** — modelos Pydantic (`ClaseData`, `AnotacionData`, `EscuelaData`) que validan el cuerpo de los requests HTTP antes de llegar al endpoint.
- **`src/Clase.py`, `src/Anotacion.py`** — clases de dominio originales, mantenidas para preservar la lógica de negocio separada del ORM.

### Relación Clase ↔ Anotación
`ClaseDB` tiene una FK opcional (`anotacion`) que apunta a `AnotacionDB.id`. La anotación es nullable: una clase puede existir sin anotación. Cuando se agrega una anotación (`POST /clases/{id}/anotacion`), se crea el registro en la tabla `anotacion` y se actualiza la FK en `clases`. Si ya existe, el mismo endpoint la actualiza (`PUT /clases/{id}/anotacion`).

Esta decisión evita la complejidad de una relación many-to-many innecesaria: cada clase tiene como máximo una anotación activa.

### Búsqueda por ID en O(1)
Las clases se identifican con un `id` entero autogenerado por SQLite (autoincrement). Los endpoints usan `db.query(ClaseDB).filter(ClaseDB.id == clase_id).first()` en lugar de iterar la lista completa, aprovechando el índice primario de la BD.

### Validación de integridad referencial en escuelas
Antes de eliminar una escuela, el backend verifica si tiene clases asociadas con un `COUNT`. Si las tiene, devuelve `409 Conflict` con un mensaje descriptivo. Esto previene errores de constraint de FK en SQLite y da feedback claro al usuario.

### Agrupación por mes con `datetime`
El endpoint `GET /clases/por-mes` usa `datetime.strptime(fecha, "%Y-%m-%d")` para parsear fechas y agrupar por `"Mes YYYY"` (ej: `"Marzo 2026"`). Se eligió `datetime` sobre manipulación manual de strings por ser más legible, validar el formato automáticamente, y facilitar operaciones futuras sobre fechas. El resultado se ordena cronológicamente usando `(año, índice_mes)` como clave de sort.

### Frontend sin frameworks
El frontend usa JavaScript vanilla con `fetch` API. La decisión fue mantener cero dependencias de build: los archivos HTML se sirven directamente desde FastAPI con `StaticFiles`. Cada página es autónoma y se comunica con la API REST del backend.

La navegación entre páginas usa `?claseId=X` como query param para pasar contexto entre vistas (ej: desde el modal de detalle en `clases.html` al formulario de `anotacion.html`).

---

## Instalación y ejecución

### Requisitos
- Python 3.8+

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Fedejalife99/Gestor-de-anotaciones.git
cd Gestor-de-anotaciones

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar el servidor
python main.py
```

La app estará disponible en **http://localhost:8000**

> La base de datos SQLite (`anotaciones.db`) se crea automáticamente en el primer arranque. Está en `.gitignore` — no se sube al repositorio.

---

## API Reference

### Clases

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/clases` | Crear nueva clase |
| `GET` | `/clases` | Listar todas las clases |
| `GET` | `/clases/{id}` | Obtener clase por ID |
| `DELETE` | `/clases/{id}` | Eliminar clase |
| `GET` | `/clases/por-mes` | Clases agrupadas cronológicamente por mes |

### Anotaciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/clases/{id}/anotacion` | Crear anotación para una clase |
| `PUT` | `/clases/{id}/anotacion` | Actualizar anotación existente |

### Escuelas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/escuelas` | Listar todas las escuelas |
| `POST` | `/escuelas` | Crear nueva escuela |
| `DELETE` | `/escuelas` | Eliminar escuela (falla con 409 si tiene clases) |

> Documentación interactiva disponible en **http://localhost:8000/docs**

---

## Modelo de datos

```
EscuelaDB
├── id (PK)
├── nombre (único)
└── fecha_creacion

ClaseDB
├── id (PK)
├── fecha (YYYY-MM-DD)
├── depto
├── escuela (FK → EscuelaDB.nombre)
├── grado
├── letra
├── nombreMaestra
├── anotacion (FK → AnotacionDB.id, nullable)
└── fecha_creacion

AnotacionDB
├── id (PK)
├── dictada (bool)
├── correspondePago (bool)
├── registroClase (texto)
└── observaciones (texto, opcional)
```

---

## Próximas mejoras

- [ ] Exportación a CSV / PDF

