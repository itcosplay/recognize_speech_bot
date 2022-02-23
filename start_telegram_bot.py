import logging

from environs import Env

from bot_scripts import start_bot


logger = logging.getLogger(__file__)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    logging.basicConfig (
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    start_bot()