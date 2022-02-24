from environs import Env

from dialogflow_scripts import train_dialog_flow


if __name__ == '__main__':
    env = Env()
    env.read_env()

    train_dialog_flow(env('GOOGLE_PROJECT_ID'))

    print('Bot was trained successfully!')