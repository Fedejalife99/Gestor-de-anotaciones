
class Anotacion:
    def __init__(self, dictada, RegistroDeClase, correspondePago):
        self.dictada = dictada
        self.RegistroDeClase = RegistroDeClase
        self.correspondePago = correspondePago
        self.observaciones = None

    def agregar_observaciones(self, observaciones):
        self.observaciones = observaciones
    def modificarRegistroDeClase(self, RegistroDeClase):
        self.RegistroDeClase = RegistroDeClase
    def modificarCorrespondePago(self, correspondePago):
        self.correspondePago = correspondePago
    