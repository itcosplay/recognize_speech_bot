import os
import logging
import pprint
import json
import requests

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
from google import api_core


logger = logging.getLogger(__file__)



def create_intent(
    project_id,
    display_name,
    training_phrases_parts,
    message_texts
):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent, 'language_code': 'ru'},
        
    )

    print('Intent was created!')


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
    env = Env()
    env.read_env()

    questions = [
        "Как устроиться к вам на работу?",
        "Как устроиться к вам?",
        "Как работать у вас?",
        "Хочу работать у вас",
        "Возможно-ли устроиться к вам?",
        "Можно-ли мне поработать у вас?",
        "Хочу работать редактором у вас"
    ]

    # answer = 'Если вы забанены, вы нарушили правила нашего сообщества. При входе на сайт вы можете увидеть доказательства ваших нарушений и ссылку на нарушенное правило. Разбан не продаётся. Если вы ознакомились с правилами и доказательствами вашей вины и у вас всё ещё есть претензии — воспользуйтесь формой «Не виновен» под сообщением о бане.'
    answer = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    print([answer])
    # try:
    #     create_intent(
    #         'recognize-speech-bot-lgeb',
    #         display_name='Устройство на работу',
    #         training_phrases_parts=questions,
    #         message_texts=[answer]
    #         # message_answer = [intents[intent]['answer']]
    #     )
    # except api_core.exceptions.InvalidArgument:
    #     print('Invalid arg!')
    

    # https://stackoverflow.com/questions/52332247/permissiondenied-403-iam-permission-dialogflow-intents-list

    # main()


    # with open('training_phrases.json', 'r') as file:
    #     training_phrases = json.load(file)

    # for training_phrase in training_phrases:
    #     print(training_phrase)
    #     display_name = training_phrase
    #     questions = training_phrases[training_phrase]['questions']
    #     answer = training_phrases[training_phrase]['answer']

    #     create_intent(
    #         'recognize-speech-bot-lgeb',
    #         display_name=display_name,
    #         training_phrases_parts=questions,
    #         message_texts=answer
    #     )
    #     create_intent()
        



