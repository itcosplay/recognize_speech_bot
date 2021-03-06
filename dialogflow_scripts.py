import os
import json

from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent (
        request={"session": session, "query_input": query_input}
    )

    return response.query_result


def create_intent (
    project_id,
    display_name,
    training_phrases_parts,
    message_texts
):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part (
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent (
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    intents_client.create_intent (
        request = {
            "parent": parent,
            "intent": intent,
            'language_code': os.environ['LANGUAGE_CODE']
        }
    )


def train_dialog_flow(project_id):
    with open('training_phrases.json', 'r', encoding='utf-8') as file:
        training_phrases = json.load(file)

    for training_phrase in training_phrases:
        questions = training_phrases[training_phrase]['questions']
        answer = training_phrases[training_phrase]['answer']

        create_intent (
            project_id=project_id,
            display_name=training_phrase,
            training_phrases_parts=questions,
            message_texts=[answer]
        )