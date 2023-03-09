from typing import Dict

from openai.error import *
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import Message

from chatai import ChatAI
from dictionary import *


class ChatClient:

    def __init__(self, app_name: str, api_id: str, api_hash: str, bot_token: str, proxy: dict):
        self.app = Client(name=app_name,
                          api_id=api_id,
                          api_hash=api_hash,
                          bot_token=bot_token,
                          proxy=proxy)

        self.chats: Dict[int, ChatAI] = {}

    @staticmethod
    def __handle_start_message(client, message):
        message.reply_text(text=START_MSG)

    async def __handle_reset_message(self, client, message):
        user_data = self.chats.get(message.from_user.id)

        if user_data:
            user_data.reset_chat()

        await message.reply_text(text=RESET_MSG)

    async def __handle_ask_message(self, client: Client, message: Message):
        user_id = message.from_user.id
        chatai = self.__get_chat(user_id)

        await message.reply_chat_action(ChatAction.TYPING)

        try:
            response = await chatai.send_message(message.text)
            await message.reply_text(text=response)

        except RateLimitError:
            await message.reply_text(RATE_LIMIT_ERR)

        except InvalidRequestError as error:
            await message.reply_text(UNKNOWN_ERR)
            raise error

    def __get_chat(self, user_id: int):
        if user_id not in self.chats.keys():
            self.chats[user_id] = ChatAI()
        return self.chats[user_id]

    def run(self):
        self.app.on_message(filters.command('start') & filters.private)(self.__handle_start_message)
        self.app.on_message(filters.command('reset') & filters.private)(self.__handle_reset_message)
        self.app.on_message(filters.text & filters.private)(self.__handle_ask_message)

        self.app.run()
