import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor

import openai

from config import *


class ChatAI:

    def __init__(self):
        openai.api_key = API_KEY
        self.__messages = deque(maxlen=MAX_MESSAGES)
        self.__thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        self.__loop = asyncio.get_event_loop()

    async def send_message(self, message: str):
        """
        Add user message to chat history, generate AI response and add it to chat history.
        """
        self._add_message('user', message)
        response = await self.__loop.run_in_executor(self.__thread_pool, self._generate_response)
        self._add_message('assistant', response)
        return response

    def _generate_response(self):
        """
        Generate AI response based on chat history.
        """
        chat_history = list(self.__messages)
        completion = openai.ChatCompletion.create(model=AI_MODEL, messages=chat_history)
        return completion.choices[0].message['content']

    def _add_message(self, role: str, content: str):
        """
        Add a message to chat history.
        """
        self.__messages.append({'role': role, 'content': content})

    def reset_chat(self):
        """
        Clear chat history.
        """
        self.__messages.clear()
