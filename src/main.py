from config import *
from bot import ChatClient

if __name__ == '__main__':
    chat_client = ChatClient(APP_NAME, API_ID, API_HASH, BOT_TOKEN, PROXY)
    chat_client.run()
