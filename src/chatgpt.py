import openai
from config import API_KEY, AI_MODEL


class ChatGPT:
    def __init__(self):
        openai.api_key = API_KEY
        self.messages = []

    def send_msg(self, message: str):
        user_input = message
        self.messages.append({'role': 'user', 'content': user_input})
        completion = openai.ChatCompletion.create(
            model=AI_MODEL,
            messages=self.messages
        )
        ai_response = completion.choices[0].message['content']
        self.messages.append({'role': 'assistant', 'content': ai_response})
        return ai_response

    def reset(self):
        self.messages.clear()
