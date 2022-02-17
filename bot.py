import os
import logging

from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters
)
from environs import Env


logger = logging.getLogger(__file__)


def command_start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I\'m a bot, please talk to me!'
    )


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()

    updater = Updater(os.environ['TG_BOT_TOKEN'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', command_start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()





