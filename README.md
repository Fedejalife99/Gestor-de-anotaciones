# Gestor de Anotaciones

Sistema de gestión de clases y anotaciones desarrollado con FastAPI y vanilla JavaScript.

## Descripción

Una aplicación web para registrar, gestionar y organizar clases, con información de grados, letras, escuelas y anotaciones personalizadas. El sistema permite visualizar las clases agrupadas por mes para la correspondencia de pagos.

## Características

- ✅ **Registro de Clases**: Crear nuevas clases con información detallada (fecha, departamento, escuela, grado, letra, nombre de la maestra)
- ✅ **Gestión de Escuelas**: Agregar y eliminar escuelas disponibles
- ✅ **Visualización por Mes**: Ver todas las clases agrupadas por mes
- ✅ **Anotaciones**: Agregar notas y observaciones a las clases
- ✅ **Interfaz Responsiva**: Frontend moderno con diseño intuitivo
- ✅ **API RESTful**: Backend totalmente documentado con FastAPI

## Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y de alto rendimiento
- **Pydantic** - Validación de datos y modelos
- **Uvicorn** - Servidor ASGI

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos con gradientes personalizados
- **JavaScript Vanilla** - Interactividad (sin dependencias)

### Base de Datos
- En memoria (actualmente)

## Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Fedejalife99/Gestor-de-anotaciones.git
cd Gestor-de-anotaciones
```

2. **Crear un entorno virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
python main.py
```

O directamente con uvicorn:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: **http://localhost:8000**

## Estructura del Proyecto

```
Gestor-de-anotaciones/
│
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
├── .gitignore             # Archivos a ignorar en git
│
├── src/                    # Módulo principal
│   ├── __init__.py
│   ├── Clase.py           # Modelo de datos para clases
│   ├── Escuelas.py        # Gestor de escuelas
│   ├── Grupos.py          # Gestión de grupos
│   ├── Anotacion.py       # Modelo de anotaciones
│   ├── Clases.py          # Gestión colectiva de clases
│   └── modelos.py         # Modelos Pydantic para validación
│
└── static/                # Archivos frontend
    ├── index.html         # Menú principal / Dashboard
    ├── nueva-clase.html   # Formulario para crear clase
    ├── clases.html        # Vista de todas las clases
    ├── clases-por-mes.html # Visualización por meses
    ├── escuelas.html      # Gestión de escuelas
    └── anotacion.html     # Gestión de anotaciones
```

## Endpoints API

### Clases
- `POST /clases` - Crear una nueva clase
- `GET /clases` - Obtener todas las clases
- `GET /clases/{id}` - Obtener una clase específica
- `DELETE /clases/{id}` - Eliminar una clase
- `GET /clases/por-mes` - Obtener clases agrupadas por mes

### Escuelas
- `GET /escuelas` - Obtener todas las escuelas
- `POST /escuelas` - Crear una nueva escuela
- `DELETE /escuelas/{id}` - Eliminar una escuela

### Páginas
- `GET /` - Página de inicio (menú principal)
- `GET /static/nueva-clase.html` - Formulario de nueva clase
- `GET /static/clases.html` - Vista de clases
- `GET /static/clases-por-mes.html` - Clases por mes
- `GET /static/escuelas.html` - Gestión de escuelas
- `GET /static/anotacion.html` - Gestión de anotaciones

## Uso

1. **Acceder a la aplicación**
   - Abre tu navegador y ve a `http://localhost:8000`

2. **Crear una clase**
   - Haz clic en "Nueva Clase"
   - Completa el formulario con los detalles de la clase
   - Selecciona el departamento, escuela, grado y letra
   - Haz clic en "Registrar Clase"

3. **Gestionar escuelas**
   - Ve a la sección "Escuelas"
   - Agrega nuevas escuelas o elimina las existentes

4. **Ver clases por mes**
   - Accede a "Clases por Mes" para visualizar las clases agrupadas
   - Útil para la correspondencia de pagos

5. **Agregar anotaciones**
   - Ve a la sección "Anotaciones"
   - Agrega notas personalizadas a las clases

## Configuración CORS

La aplicación permite peticiones desde cualquier origen. Esto es útil durante el desarrollo, pero para producción se recomienda configurar orígenes específicos:

```python
allow_origins=["https://tudominio.com"],
```

## Próximas Mejoras

- [ ] Implementar persistencia en base de datos (SQLite/PostgreSQL)
- [ ] Autenticación de usuarios
- [ ] Reportes PDF de clases
- [ ] Búsqueda y filtrado avanzado
- [ ] Exportación de datos (CSV, Excel)
- [ ] Tema oscuro
- [ ] Aplicación móvil

## Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.

## Contacto

**Autor**: Fede  
**Email**: fedejalife99@gmail.com  
**GitHub**: [@Fedejalife99](https://github.com/Fedejalife99)

---

**Última actualización**: Marzo 2026
