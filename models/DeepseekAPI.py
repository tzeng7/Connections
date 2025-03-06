import os

from helpers.Model import Model
from helpers.Answer import Answer

from openai import OpenAI

from dotenv import load_dotenv

import json
import re

class DeepseekLLMPrompter(Model):
    def __init__(self):
        self.configure()
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEKAI_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.history = []
        self.model = "deepseek-chat"

    def swap_model(self):
        pass
    def prompt_llm(self, input_prompt: str):
        self.history.append({
            "role": "user",
            "content": input_prompt
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history
        )

        json_text = re.findall("```json\n((.|\n)*)\n```", response.choices[0].message.content)
        json_text_answer = Answer(**json.loads(json_text[0][0]))
        self.history.append(
            response.choices[0].message
        )

        return json_text_answer

    def configure(self):
        load_dotenv()

