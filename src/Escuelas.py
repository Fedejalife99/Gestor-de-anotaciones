class Escuelas:
    def __init__(self):
        self.listaEscuelas = []
    def agregar_escuela(self, escuela:str):
        self.listaEscuelas.append(escuela)
    def eliminar_escuela(self, escuela:str):
        self.listaEscuelas.remove(escuela)
    def darEscuelas(self):
        return self.listaEscuelas
    