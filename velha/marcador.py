class Marcador(object):
    def get_tipo(self):
        return self.tipo_atual

    def get_texto(self):
        if self.tipo_atual == 0:
            return 'x'
        elif self.tipo_atual == 1:
            return '0'

    def __init__(self, tipo):
        self.tipo_atual = tipo
