from collections import deque

import openai
from config import API_KEY, AI_MODEL


class ChatGPT:
    MAX_MESSAGES = 10

    def __init__(self):
        openai.api_key = API_KEY
        self.messages = deque(maxlen=self.MAX_MESSAGES)

    def send_msg(self, message: str):
        self.messages.append({'role': 'user', 'content': message})
        completion = openai.ChatCompletion.create(
            model=AI_MODEL,
            messages=list(self.messages)
        )
        ai_response = completion.choices[0].message['content']
        self.messages.append({'role': 'assistant', 'content': ai_response})
        return ai_response

    def reset(self):
        self.messages.clear()
