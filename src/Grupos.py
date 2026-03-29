class Grupos:
    def __init__(self):
        self.listaGrupos = []
    def agregar_grupo(self, grupo):
        self.listaGrupos.append(grupo)
    def eliminar_grupo(self, grupo):
        self.listaGrupos.remove(grupo)
    def darGrupos(self):
        return self.listaGrupos