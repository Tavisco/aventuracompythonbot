class VelhaHandler(object):
    ListaDeJogosVelha = []

    def adicionar_jogo(self, jogo):
        self.ListaDeJogosVelha.append(jogo)

    def get_jogo_by_chat_id(self, chat_id):
        for jogo in self.ListaDeJogosVelha:
            if jogo.get_chat_id() == chat_id:
                return jogo
        return None

    def __init__(self):
        self.ListaDeJogosVelha = []
