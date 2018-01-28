# O Compileall no travis.yml fará o syntax checking

from velha.jogo_velha import JogoDaVelha
from velha.gameshandler import VelhaHandler

velha_handler = VelhaHandler()

tst_chat_id = 123456
user1_id = 654321
user1_name = 'Usuario 1'
user2_id = 987654
user2_name = 'Usuario 2'
tst_message_id = 11111


def func(x):
    return x + 1


def test_answer():
    if not func(3) == 4:
        raise AssertionError()


def enviar_mensagem(chat_id, text, reply_to_message_id=None, reply_markup=None):
    print('\n>>> Chat_id="' + str(chat_id) + '" Texto="' + str(text) + '" Message_id="' + str(reply_to_message_id) + '"')

def editar_mensagem(chat_id, text, message_id, reply_markup):
    print('\n>ED>> Chat_id="' + str(chat_id) + '" Texto="' + str(text) + '" Message_id="' + str(message_id) + '"')

def test_iniciar_jogo_velha():
    velha = JogoDaVelha(tst_chat_id, user1_id, user1_name, enviar_mensagem, editar_mensagem)
    velha_handler.adicionar_jogo(velha)


def test_segundo_jogador_velha():
    velha = velha_handler.get_jogo_by_chat_id(tst_chat_id)
    velha.add_jogador(user2_id, user2_name)


def test_efetuar_jogada_velha():
    velha = velha_handler.get_jogo_by_chat_id(tst_chat_id)
    velha.efetuar_jogada(user1_id, 'b_0_0', tst_message_id)
    velha.efetuar_jogada(user2_id, 'b_1_0', tst_message_id)
    velha.efetuar_jogada(user1_id, 'b_0_2', tst_message_id)
    velha.efetuar_jogada(user2_id, 'b_1_2', tst_message_id)
    velha.efetuar_jogada(user1_id, 'b_0_1', tst_message_id)
