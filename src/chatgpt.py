import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor

import openai
from config import *


class ChatGPT:

    def __init__(self):
        openai.api_key = API_KEY
        self.messages = deque(maxlen=MAX_MESSAGES)
        self.thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        self.loop = asyncio.get_event_loop()

    async def send(self, message: str):
        self.messages.append({'role': 'user', 'content': message})
        ai_response = await self.loop.run_in_executor(self.thread_pool, self.__gen_response)
        self.messages.append({'role': 'assistant', 'content': ai_response})
        return ai_response

    def __gen_response(self):
        completion = openai.ChatCompletion.create(
            model=AI_MODEL,
            messages=list(self.messages)
        )
        return completion.choices[0].message['content']

    def reset(self):
        self.messages.clear()
