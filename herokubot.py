import logging
import os
import sys
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from velha.jogo_velha import JogoDaVelha
from velha.gameshandler import VelhaHandler

velha_handler = VelhaHandler()
tg_bot = None


def start(bot, update):
    update.effective_message.reply_text("Hi!")


def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)


def helpme(bot, update):
    update.message.reply_text("Digite uma mensagem que eu irei repeti-la!")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def piada(bot, update):
    update.effective_message.reply_text("Sabe qual é o meu nome? Irineu. Você não sabe nem eu KKKKKKKK")


def charada(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    req_headers = {'Accept': 'application/json'}
    req_url = 'https://us-central1-kivson.cloudfunctions.net/charada-aleatoria'
    req_charada = requests.get(req_url, headers=req_headers)
    if req_charada.status_code != 200:
        update.message.reply_text("Ocorreu um erro ao tentar obter a charada :c")
    else:
        obj_charada = req_charada.json()
        update.message.reply_text(obj_charada["pergunta"])
        update.message.reply_text(obj_charada["resposta"])


def host(bot, update):
    if len(sys.argv) > 1:
        update.message.reply_text('Estou rodando no Heroku!')
    else:
        update.message.reply_text('Estou rodando localmente!')


def botoes(bot, update):
    custom_keyboard = [['top-left', 'top-right'],
                       ['bottom-left', 'bottom-right']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text='Teste de teclado', reply_markup=reply_markup)


def no_botoes(bot, update):
    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=update.message.chat_id, text='Removendo botoes...', reply_markup=reply_markup)


def enviar_mensagem(chat_id, text, reply_to_message_id=None, reply_markup=None):
    tg_bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)


def editar_mensagem(chat_id, text, message_id, reply_markup):
    tg_bot.edit_message_text(text=text,
                             chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)


def novo_velha(bot, update):
    velha = JogoDaVelha(update.message.chat_id, update.effective_user.id,
                        update.effective_user.first_name, enviar_mensagem, editar_mensagem)
    velha_handler.adicionar_jogo(velha)


def entrar_velha(bot, update):
    velha = velha_handler.get_jogo_by_chat_id(update.message.chat_id)
    velha.add_jogador(update.effective_user.id, update.effective_user.first_name)


def tratar_uso_inline(bot, update):
    query = update.callback_query

    # Vamos verificar se essa mensagem esta em um jogo da velha
    velha = velha_handler.get_jogo_by_chat_id(query.message.chat_id)
    if velha is not None:
        # Logo o essa mensagem veio de um jogo da velha
        velha.efetuar_jogada(update.effective_user.id, query.data, query.message.message_id)
    else:
        bot.send_message(chat_id=query.message.chat_id, text='N foi encontrado um jogo da velha...')


if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = "511552531:AAHWTIk89QXtsCGyNOX7zxClY0UwO93zsVE"
    NAME = "aventuracompythonbot"

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    tg_bot = updater.bot

    # Add command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', helpme))
    dp.add_handler(CommandHandler('piada', piada))
    dp.add_handler(CommandHandler('charada', charada))
    dp.add_handler(CommandHandler('host', host))
    dp.add_handler(CommandHandler('botoes', botoes))
    dp.add_handler(CommandHandler('noBotoes', no_botoes))
    dp.add_handler(CommandHandler('novoVelha', novo_velha))
    dp.add_handler(CommandHandler('entrarVelha', entrar_velha))
    dp.add_handler(CallbackQueryHandler(tratar_uso_inline))

    # Add noncommand handlers
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Add error handler to log all errors
    dp.add_error_handler(error)

    if len(sys.argv) > 1:
        # Running on Heroku!

        # Port is given by Heroku
        PORT = os.environ.get('PORT')
        # Start the webhook
        print("Starting bot on Heroku...")
        updater.start_webhook(listen="0.0.0.0",
                              port=int(PORT),
                              url_path=TOKEN)
        updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    else:
        # Running locally
        print("Starting bot locally...")
        updater.start_polling()

    updater.idle()
