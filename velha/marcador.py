class Marcador(object):
    def get_tipo(self):
        return self.tipo_atual

    def get_texto(self):
        if self.tipo_atual == 0:
            return 'X'
        elif self.tipo_atual == 1:
            return 'O'

    def get_emoji(self):
        if self.tipo_atual == 0:
            return '❌'
        elif self.tipo_atual == 1:
            return '⭕'

    def __init__(self, tipo):
        self.tipo_atual = tipo
