import logging
import os
import sys
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


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
    reqHeaders = {'Accept': 'application/json'}
    reqUrl = 'https://us-central1-kivson.cloudfunctions.net/charada-aleatoria'
    reqCharada = requests.get(reqUrl, headers=reqHeaders)
    if reqCharada.status_code != 200:
        update.message.reply_text("Ocorreu um erro ao tentar obter a charada :c")
    else:
        charada = reqCharada.json()
        update.message.reply_text(charada["pergunta"])
        update.message.reply_text(charada["resposta"])


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


def inline_keyboard(bot, update):
    button_list = [
        InlineKeyboardButton(" ", callback_data='b_0_0'),
        InlineKeyboardButton(" ", callback_data='b_0_1'),
        InlineKeyboardButton(" ", callback_data='b_0_2'),
        InlineKeyboardButton(" ", callback_data='b_1_0'),
        InlineKeyboardButton(" ", callback_data='b_1_1'),
        InlineKeyboardButton(" ", callback_data='b_1_2'),
        InlineKeyboardButton(" ", callback_data='b_2_1'),
        InlineKeyboardButton(" ", callback_data='b_2_2'),
        InlineKeyboardButton(" ", callback_data='b_2_3')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
    bot.send_message(chat_id=update.message.chat_id, text="É a vez do " + update.effective_user.first_name, reply_markup=reply_markup)


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


def tratador_inlinekb(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="{} selecionou: {}".format(update.effective_user.first_name, query.data),
                          chat_id=query.message.chat_id, message_id=query.message.message_id)


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

    # Add command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', helpme))
    dp.add_handler(CommandHandler('piada', piada))
    dp.add_handler(CommandHandler('charada', charada))
    dp.add_handler(CommandHandler('host', host))
    dp.add_handler(CommandHandler('botoes', botoes))
    dp.add_handler(CommandHandler('noBotoes', no_botoes))
    dp.add_handler(CommandHandler('inlinekb', inline_keyboard))
    dp.add_handler(CallbackQueryHandler(tratador_inlinekb))

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
