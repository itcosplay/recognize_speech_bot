import os
import random
import vk_api

from environs import Env

from vk_api.longpoll import VkLongPoll, VkEventType

from dilogflow_scripts import detect_intent_texts


def echo (event, vk_api):
    project_id = os.environ['GOOGLE_PROJECT_ID']

    answer = detect_intent_texts (
        project_id=project_id,
        session_id=event.user_id,
        text=event.text,
        language_code='ru'
    )

    vk_api.messages.send (
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1,1000)
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    vk_session = vk_api.VkApi(token=os.environ['VK_GROUP_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)