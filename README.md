# бот с распознаванием фраз
Бот реализованый для vk и telegram с возможностью обучения.

Возможности бота:
- Бот умеет различать приветсявия;
- Бота можно обучить различать фразы с можностью добавления ответов на фразы.

Перед установкой бота создайте аккаунт на [DialogFlow](https://dialogflow.cloud.google.com/#/getStarted)



## Необходимое окружение
|переменная|описание|тип
|----------|--------|--------------
|`TG_BOT_TOKEN`|Токен для бота [telegram](https://core.telegram.org/bots#6-botfather)|string
|`GOOGLE_APPLICATION_CREDENTIALS`|Путь к файлу с [credentials](https://cloud.google.com/docs/authentication/getting-started)|'string.json'
|`LANGUAGE_CODE`|Язык обучения для [DialogFlow](https://cloud.google.com/dialogflow/es/docs/reference/language)|string
|`GOOGLE_PROJECT_ID`|id проекта в [credentials](https://cloud.google.com/docs/authentication/getting-started)|string
|`VK_GROUP_TOKEN`|Токен вашей [группы vk](https://pechenek.net/social-networks/vk/api-vk-poluchaem-klyuch-dostupa-token-gruppy/)|string

Все переменные окружения должны храниться в файле .env в корне проекта.

## Как установить
* Клонируем репозиторий
* Добавляем файл .env с необходимыми переменными
* Создаем виртуальное окружение
* Устанавливаем зависимости
```
pip install -r requirements.txt
```

## Запуск
Запуск бота в telegram:
```
python start_telegram_bot.py
```

Запуск бота в vk:
```
python start_vk_bot.py
```


## Обучение бота
Сохраните в корне проекта json файл с названием `training_phrases.json`
Структара файла:
```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
}
```
Запустите скрипт обучения:
```
python train_bots.py
```

## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
