import os
import random
import logging

from environs import Env

from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_scripts import detect_intent_texts


logger = logging.getLogger(__file__)


def answer_from_dialog_flow (event, vk_api):
    project_id = os.environ['GOOGLE_PROJECT_ID']
    language_code = os.environ['LANGUAGE_CODE']

    answer = detect_intent_texts (
        project_id=project_id,
        session_id=event.user_id,
        text=event.text,
        language_code=language_code
    )

    if not answer.intent.is_fallback:
        vk_api.messages.send (
            user_id=event.user_id,
            message=answer.fulfillment_text,
            random_id=random.randint(1,1000)
        )


def main():
    env = Env()
    env.read_env()

    logging.basicConfig (
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    vk_session = vk_api.VkApi(token=os.environ['VK_GROUP_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_from_dialog_flow(event, vk_api)


if __name__ == '__main__':
    try:
        main()

    except Exception as error:
        logger.error(error)