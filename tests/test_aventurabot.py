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


def enviar_mensagem(chat_id, text, reply_to_message_id=None, reply_markup=None):
    print('\n>>> Chat_id="' + str(chat_id) + '" Texto="' + str(text) + '" Message_id="'
          + str(reply_to_message_id) + '"')


def editar_mensagem(chat_id, text, message_id, reply_markup=None):
    print('\n>ED>> Chat_id="' + str(chat_id) + '" Texto="' + str(text) + '" Message_id="' + str(message_id) + '"')


def terminar_jogo_velha(chat_id):
    velha = velha_handler.get_jogo_by_chat_id(chat_id)
    if velha is not None:
        txt_mensagem = ''

        if velha.get_index_player_ganhador() != -1:
            txt_mensagem += velha.obter_jogador(velha.get_index_player_ganhador()).nome + ' ganhou essa partida!'

        elif velha.contagem == 9:
            txt_mensagem += 'Deu velha!'

        print('\n>FIM>> Chat_id="' + str(chat_id) + '" Texto="' + str(txt_mensagem))
        velha_handler.remover_jogo(velha)


def iniciar_jogo_velha(uid, name):
    velha = JogoDaVelha(tst_chat_id, uid, name, enviar_mensagem, editar_mensagem, terminar_jogo_velha)
    velha_handler.adicionar_jogo(velha)


def adicionar_segundo_jogador(uid, name):
    velha = velha_handler.get_jogo_by_chat_id(tst_chat_id)
    velha.add_jogador(uid, name)


def test_user1_ganhar_horizontal():
    print('------ User1 horizontal ------')
    iniciar_jogo_velha(user1_id, user1_name)
    velha = velha_handler.get_jogo_by_chat_id(tst_chat_id)

    if velha.jogo_em_andamento:
        # Verifico se o jogo iniciou com 1 jogador apenas
        raise AssertionError()

    adicionar_segundo_jogador(user2_id, user2_name)
    if not velha.jogo_em_andamento:
        # Verifico se o jogo não iniciou com 2 jogadores
        raise AssertionError()

    velha.efetuar_jogada(user1_id, 'b_0_0', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_1_0', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user1_id, 'b_0_2', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_1_2', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user1_id, 'b_0_1', tst_message_id)

    if velha.jogo_em_andamento:
        # user1 ganhou a partida, logo verifico se ela nao
        # esta mais em andamento
        raise AssertionError()

    if not velha.jogador_atual == 0:
        # E agora verifico se foi o user1 que realmente
        # ganhou a partida
        raise AssertionError()


def test_user2_ganhar_vertical():
    print('------ User2 vertical ------')
    iniciar_jogo_velha(user1_id, user1_name)
    velha = velha_handler.get_jogo_by_chat_id(tst_chat_id)

    if velha.jogo_em_andamento:
        # Verifico se o jogo iniciou com 1 jogador apenas
        raise AssertionError()

    adicionar_segundo_jogador(user2_id, user2_name)
    if not velha.jogo_em_andamento:
        # Verifico se o jogo não iniciou com 2 jogadores
        raise AssertionError()

    velha.efetuar_jogada(user1_id, 'b_0_0', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_1_0', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user1_id, 'b_2_0', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_1_1', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user1_id, 'b_2_2', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_1_2', tst_message_id)

    if velha.jogo_em_andamento:
        # user1 ganhou a partida, logo verifico se ela nao
        # esta mais em andamento
        raise AssertionError()

    if not velha.jogador_atual == 1:
        # E agora verifico se foi o user2 que realmente
        # ganhou a partida
        raise AssertionError()


def test_velha():
    print('------ Velha ------')
    iniciar_jogo_velha(user1_id, user1_name)
    velha = velha_handler.get_jogo_by_chat_id(tst_chat_id)

    if velha.jogo_em_andamento:
        # Verifico se o jogo iniciou com 1 jogador apenas
        raise AssertionError()

    adicionar_segundo_jogador(user2_id, user2_name)
    if not velha.jogo_em_andamento:
        # Verifico se o jogo não iniciou com 2 jogadores
        raise AssertionError()

    velha.efetuar_jogada(user1_id, 'b_0_0', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_0_1', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user1_id, 'b_0_2', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_1_0', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user1_id, 'b_1_2', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_1_1', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user1_id, 'b_2_0', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user2_id, 'b_2_2', tst_message_id)
    if not velha.jogo_em_andamento:
        raise AssertionError()
    velha.efetuar_jogada(user1_id, 'b_2_1', tst_message_id)

    if velha.jogo_em_andamento:
        # a partida NAO deve estar em andamento
        raise AssertionError()

    if velha.contagem != 9:
        # a contagem DEVE ser 9
        raise AssertionError()


def test_mesmo_player_2x():
    iniciar_jogo_velha(user1_id, user1_name)
    velha = velha_handler.get_jogo_by_chat_id(tst_chat_id)
    if not len(velha.jogadores) == 1:
        raise AssertionError()
    # TODO: Terminar esse teste


