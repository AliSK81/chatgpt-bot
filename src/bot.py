from openai.error import RateLimitError, InvalidRequestError
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import Message
from dictionary import *

from chatgpt import ChatGPT
from config import *

chats = dict()

app = Client(name=APP_NAME,
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             proxy=PROXY)


@app.on_message(filters.command('start') & filters.private)
async def reset(client, message):
    await message.reply_text(text=START_MSG)


@app.on_message(filters.command('reset') & filters.private)
async def reset(client, message):
    user_id = message.from_user.id

    if user_id in chats.keys():
        chats[user_id].reset()

    await message.reply_text(text=RESET_MSG)


@app.on_message(filters.text & filters.private)
async def ask(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id not in chats.keys():
        chats[user_id] = ChatGPT()

    chat = chats[user_id]

    await message.reply_chat_action(ChatAction.TYPING)

    try:
        ai_response = chat.send_msg(message.text)
        await message.reply_text(text=ai_response)

    except RateLimitError:
        await message.reply_text(RATE_LIMIT_ERR)
    except InvalidRequestError:
        chat.reset()
