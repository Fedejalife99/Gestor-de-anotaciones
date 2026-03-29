from datetime import datetime

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

class Clase:
    def __init__(self, fecha=None, depto=None, escuela=None, grado=None, letra=None, nombreMaestra=None, anotacion=None):
        self._fecha = fecha
        self._depto = depto
        self._escuela = escuela
        self._grado = grado
        self._letra = letra
        self._nombreMaestra = nombreMaestra
        self._anotacion = anotacion

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        self._fecha = value

    @property
    def depto(self):
        return self._depto

    @depto.setter
    def depto(self, value):
        self._depto = value

    @property
    def escuela(self):
        return self._escuela

    @escuela.setter
    def escuela(self, value):
        self._escuela = value

    @property
    def grado(self):
        return self._grado

    @grado.setter
    def grado(self, value):
        self._grado = value

    @property
    def letra(self):
        return self._letra

    @letra.setter
    def letra(self, value):
        self._letra = value

    @property
    def nombreMaestra(self):
        return self._nombreMaestra

    @nombreMaestra.setter
    def nombreMaestra(self, value):
        self._nombreMaestra = value

    @property
    def anotacion(self):
        return self._anotacion

    @anotacion.setter
    def anotacion(self, value):
        self._anotacion = value

    def modificarAnotacion(self, nueva_anotacion):
        self._anotacion = nueva_anotacion

    # ── Almacenamiento en memoria como diccionario {id: Clase} ──
    _clases_registradas: dict = {}
    _contador_id: int = 0

    @classmethod
    def registrar(cls, clase) -> int:
        """Guarda la clase y retorna el ID asignado."""
        cls._contador_id += 1
        cls._clases_registradas[cls._contador_id] = clase
        return cls._contador_id

    @classmethod
    def buscarPorId(cls, clase_id: int):
        """Retorna la instancia de Clase con ese ID, o None si no existe."""
        return cls._clases_registradas.get(clase_id)

    @classmethod
    def _clase_a_dict(cls, id_: int, c) -> dict:
        """Convierte una instancia de Clase a dict JSON-serializable."""
        anotacion_dict = None
        if c._anotacion:
            anotacion_dict = {
                "dictada":        c._anotacion.dictada,
                "registroDeClase": c._anotacion.RegistroDeClase,
                "correspondePago": c._anotacion.correspondePago,
                "observaciones":  c._anotacion.observaciones,
            }
        return {
            "id":           id_,
            "fecha":        c._fecha,
            "depto":        c._depto,
            "escuela":      c._escuela,
            "grado":        c._grado,
            "letra":        c._letra,
            "nombreMaestra": c._nombreMaestra,
            "anotacion":    anotacion_dict,
        }

    @classmethod
    def darClases(cls) -> list:
        """Retorna lista de dicts con id incluido, listos para JSON."""
        return [cls._clase_a_dict(id_, c) for id_, c in cls._clases_registradas.items()]

    @classmethod
    def darClasesPorMes(cls) -> dict:
        """
        Retorna un dict ordenado cronológicamente:
        {
            "Marzo 2026":    [ {clase}, ... ],
            "Abril 2026":    [ {clase}, ... ],
            "sin-fecha":     [ {clase}, ... ],  # solo si las hay
        }
        """
        agrupado: dict = {}
        orden: dict = {}  # clave_display -> (year, month) para ordenar

        for id_, c in cls._clases_registradas.items():
            try:
                dt = datetime.strptime(c._fecha, "%Y-%m-%d")
                clave = f"{MESES[dt.month - 1]} {dt.year}"  # "Marzo 2026"
                orden[clave] = (dt.year, dt.month)
            except (TypeError, ValueError):
                clave = "sin-fecha"
                orden[clave] = (9999, 99)  # al final

            if clave not in agrupado:
                agrupado[clave] = []
            agrupado[clave].append(cls._clase_a_dict(id_, c))

        # Ordenar cronológicamente por (year, month)
        return dict(sorted(agrupado.items(), key=lambda kv: orden[kv[0]]))
