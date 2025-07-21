import json
import re

from dotenv import load_dotenv

import os
from google import genai
from google.genai import types

from helpers.Answer import Answer
from helpers.Model import Model


class GeminiLLMPrompter(Model):
    def __init__(self):
        self.configure()
        self.client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
        self.chat_session = self.client.chats.create(
            model="gemini-2.5-pro-preview-06-05",
        )
        self.history = []
        self.uses_flash = True

    def swap_model(self):
        if self.uses_flash:
            print("Switching to pro")
            self.chat_session = self.client.chats.create(
                model="gemini-2.0-flash",
                history=self.history
            )
            self.uses_flash = False
        else:
            print("Switching to flash")
            self.chat_session = self.client.chats.create(
                model="gemini-2.0-flash",
                history=self.history
            )
            self.uses_flash = True

    # Create the model
    def prompt_llm(self, input_prompt: str) -> Answer:
        self.history.append(types.Content(
            parts=[types.Part.from_text(text=input_prompt)],
            role="user"
        ))
        response = self.chat_session.send_message(input_prompt)

        json_text = re.findall("```json\n((.|\n)*)\n```", response.text)[0][0]
        json_text_answer = Answer(**json.loads(json_text))
        self.history.append(types.Content(
            parts=[types.Part.from_text(text=f'[{",".join(json_text_answer.answer)}]'),
                   types.Part.from_text(text=json_text_answer.reason)],
            role="model"
        ))

        return json_text_answer

    def configure(self):
        load_dotenv()

    def to_string(self):
        return "Gemini"
