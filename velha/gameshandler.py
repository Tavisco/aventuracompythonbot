from velha.jogo_velha import JogoDaVelha


class VelhaHandler(object):
    ListaDeJogosVelha = []

    def adicionar_jogo(self, jogo):
        self.ListaDeJogosVelha.append(jogo)

    def get_jogo_by_chat_id(self, chat_id) -> JogoDaVelha:
        for jogo in self.ListaDeJogosVelha:
            if jogo.get_chat_id() == int(chat_id):
                return jogo
        return None

    def remover_jogo(self, jogo):
        self.ListaDeJogosVelha.remove(jogo)

    def __init__(self):
        self.ListaDeJogosVelha = []
