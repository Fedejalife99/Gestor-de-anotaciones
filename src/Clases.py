from datetime import datetime
        
class Clases:
    def __init__(self):
        self._clases = {}
    
    def agregar_clase(self, clase):
        self._clases[clase.id] = clase
    
    def darClases(self):
        return self._clases
    
    def darClasesPorMes(self, mes: int, anno: int):     
        clases_mes = []
        
        for clase in self._clases.values():
            try:
                fecha_obj = datetime.strptime(clase.fecha, "%Y-%m-%d")
                if fecha_obj.month == mes and fecha_obj.year == anno:
                    if clase.anotacion.correspondePago:
                        clases_mes.append(clase)
            except (TypeError, ValueError):
                continue
        
        return clases_mes
