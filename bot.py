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
from google.cloud import dialogflow


logger = logging.getLogger(__file__)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    print(response.query_result.fulfillment_text)

    return response.query_result.fulfillment_text


def command_start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I\'m a bot, please talk to me!'
    )


def echo(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_text = update.message.text

    answer = detect_intent_texts(
        'recognize-speech-bot-lgeb',
        user_id,
        user_text,
        'ru'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer
    )


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

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




