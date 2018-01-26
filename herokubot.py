import logging
import os
import sys
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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
    #bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
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
