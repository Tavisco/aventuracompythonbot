import logging

from velha.jogador import Jogador


class JogoDaVelha(object):

    def get_chat_id(self):
        return self.chat_id

    def add_jogador(self, user_id, nome):
        self.logger.debug('Adicionando "' + nome + '" ao jogo')
        marcador = 0
        if len(self.jogadores) == 1:
            marcador = 1
        jogador = Jogador(user_id, nome, marcador)
        self.jogadores.append(jogador)
        texto = self.get_jogador_by_user_id(user_id).get_nome() + ' joga como ' + self.get_jogador_by_user_id(
            user_id).get_marcador().get_texto()
        self.send_message(self.chat_id, texto)

    def get_jogador_by_user_id(self, user_id):
        for jogador in self.jogadores:
            if jogador.user_id == user_id:
                return jogador
        return None

    def __init__(self, chat_id, user_id, nome, send_message):
        self.jogadores = []
        self.chat_id = chat_id
        self.current_player = 0
        self.send_message = send_message
        self.logger = logging.getLogger(__name__)

        self.add_jogador(user_id, nome)
        self.send_message(self.chat_id, 'Jogo da velha iniciado! Aguardando próximo jogador...')
