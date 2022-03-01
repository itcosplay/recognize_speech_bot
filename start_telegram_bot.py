import os
import logging

from environs import Env

from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters
)

from dialogflow_scripts import detect_intent_texts


logger = logging.getLogger(__file__)


def command_start(update: Update, context: CallbackContext):
    context.bot.send_message (
        chat_id=update.effective_chat.id,
        text='I\'m a bot, please talk to me!'
    )


def answer_from_dialog_flow(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_text = update.message.text
    project_id = os.environ['GOOGLE_PROJECT_ID']

    answer = detect_intent_texts (
        project_id=project_id,
        session_id=user_id,
        text=user_text,
        language_code='ru'
    )
    context.bot.send_message (
        chat_id=update.effective_chat.id,
        text=answer.fulfillment_text
    )


def main():
    env = Env()
    env.read_env()

    logging.basicConfig (
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    updater = Updater(os.environ['TG_BOT_TOKEN'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', command_start))
    dispatcher.add_handler (
        MessageHandler (
            Filters.text & ~Filters.command,
            answer_from_dialog_flow
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()