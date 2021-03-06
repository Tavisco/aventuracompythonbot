import logging

import numpy as np

from velha.jogador import Jogador
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


class JogoDaVelha(object):

    def obter_jogador(self, index) -> Jogador:
        return self.jogadores[index]

    def get_index_player_ganhador(self):
        if not self.jogo_em_andamento and self.jogador_atual != -1 and not self.velha:
            return self.jogador_atual

        return -1

    def get_chat_id(self):
        return self.chat_id

    def jogador_ja_existe(self, user_id):
        for jogador in self.jogadores:
            if jogador.user_id == user_id:
                return True

        return False

    def add_jogador(self, user_id, nome):
        marcador = 0
        if len(self.jogadores) == 1:
            marcador = 1
        jogador = Jogador(user_id, nome, marcador)
        self.jogadores.append(jogador)

        texto = jogador.nome + ' joga como ' + jogador.marcador.get_texto()
        self.send_message(self.chat_id, texto)

        if len(self.jogadores) == 2:
            self.send_message(self.chat_id, 'Começando jogo!')
            self.jogador_atual = 0
            self.jogo_em_andamento = True
            reply_markup = self.montar_inline_keyboard()
            self.send_message(chat_id=self.chat_id, text="É a vez de " + self.obter_jogador(self.jogador_atual).nome,
                              reply_markup=reply_markup)

    def verifica_ganhadores(self, x, y):
        # Verifica se ganhou na horizontal
        horizontal = self.tabuleiro[x][0] == self.tabuleiro[x][1] == self.tabuleiro[x][2] == self.tabuleiro[x][y]
        if horizontal:
            return True

        # Verifica se ganhou na vertical
        vertical = self.tabuleiro[0][y] == self.tabuleiro[1][y] == self.tabuleiro[2][y] == self.tabuleiro[x][y]
        if vertical:
            return True

        # Verifica se ganhou na diagonal esquerda-direita
        diag1 = self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] == self.tabuleiro[x][y]
        if diag1:
            return True

        # Verifica se ganhou na diagonal direita-esquerda
        diag2 = self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] == self.tabuleiro[x][y]
        if diag2:
            return True

        return False

    def montar_inline_keyboard(self):
        button_list = []
        for y in range(0, 3):
            for x in range(0, 3):
                button_list.append(InlineKeyboardButton(self.tabuleiro[x][y], callback_data='b_' + str(x) +
                                                                                            '_' + str(y)))

        return InlineKeyboardMarkup(build_menu(button_list, n_cols=3))

    def atualiza_tabuleiro(self, message_id):
        reply_markup = self.montar_inline_keyboard()
        if self.get_index_player_ganhador() == -1 and not self.velha:
            self.edit_message(chat_id=self.chat_id, text='É a vez de ' + self.obter_jogador(self.jogador_atual).nome,
                              message_id=message_id, reply_markup=reply_markup)
        elif self.get_index_player_ganhador() != -1:
            self.edit_message(chat_id=self.chat_id, text='Jogo finalizado! ' +
                                                         self.obter_jogador(self.jogador_atual).nome + ' venceu!',
                              message_id=message_id, reply_markup=reply_markup)
        elif self.velha:
            self.edit_message(chat_id=self.chat_id, text='Deu velha!',
                              message_id=message_id, reply_markup=reply_markup)

    def efetuar_jogada(self, user_id, posicao, message_id):
        jogador = self.jogadores[self.jogador_atual]
        if jogador.user_id != user_id:
            self.send_message(self.chat_id, 'Jogador incorreto!')
            return

        self.contagem += 1

        coord_posicao = posicao.split('_')
        coord_x = int(coord_posicao[1])
        coord_y = int(coord_posicao[2])

        self.tabuleiro[coord_x][coord_y] = jogador.marcador.get_texto()

        ganhou = self.verifica_ganhadores(x=coord_x, y=coord_y)

        if ganhou:
            self.jogo_em_andamento = False
            self.terminar_jogo(chat_id=self.chat_id)
        else:
            if self.jogador_atual == 0:
                self.jogador_atual = 1
            else:
                self.jogador_atual = 0

        if self.contagem == 9:
            self.jogo_em_andamento = False
            self.velha = True
            self.terminar_jogo(chat_id=self.chat_id)

        self.atualiza_tabuleiro(message_id)

    def __init__(self, chat_id, user_id, nome, send_message, edit_message, terminar_jogo):
        self.jogadores = []
        self.tabuleiro = np.full((3, 3), " ")
        self.chat_id = chat_id
        self.jogador_atual = -1
        self.contagem = 0
        self.jogo_em_andamento = False
        self.velha = False
        self.send_message = send_message
        self.edit_message = edit_message
        self.terminar_jogo = terminar_jogo
        self.logger = logging.getLogger(__name__)

        self.add_jogador(user_id, nome)
        self.send_message(self.chat_id, 'Jogo da velha iniciado! Aguardando próximo jogador '
                                        '(digite /entrarVelha para entrar)')


