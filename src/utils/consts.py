import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    TIMEOUT = 30
