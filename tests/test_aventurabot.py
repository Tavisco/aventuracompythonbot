# Enquanto não desenvolvo a lógica
# do jogo da velha, esse teste será
# bem dummy
#
# O Compileall no travis.yml fará o syntax checking

from velha.jogo_velha import JogoDaVelha
from velha.gameshandler import VelhaHandler

velha_handler = VelhaHandler()

chat_id = 123456
user1_id = 654321
user1_name = 'Usuario 1'
user2_id = 987654
user2_name = 'Usuario 2'


def func(x):
    return x + 1


def test_answer():
    if not func(3) == 4:
        raise AssertionError()


def enviar_mensagem(msg_chat_id, texto, message_id=None):
    print('\n>>> Chat_id="' + str(msg_chat_id) + '" Texto="' + texto + '" Message_id="' + str(message_id) + '"')


def test_iniciar_jogo_velha():
    velha = JogoDaVelha(chat_id, user1_id, user1_name, enviar_mensagem)
    velha_handler.adicionar_jogo(velha)


def test_segundo_jogador_velha():
    velha = velha_handler.get_jogo_by_chat_id(chat_id)
    velha.add_jogador(user2_id, user2_name)


