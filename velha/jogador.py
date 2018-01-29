from velha.marcador import Marcador


class Jogador(object):

    def __init__(self, user_id, nome, marcador):
        self.user_id = user_id
        self.nome = nome
        self.marcador = Marcador(marcador)
