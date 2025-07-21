import os

from helpers.Model import Model
from helpers.Answer import Answer

from openai import OpenAI

from dotenv import load_dotenv

import json
import re

system_prompt = open("system_prompt.txt").read()

class DeepseekLLMPrompter(Model):
    def __init__(self):
        self.configure()
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEKAI_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.history = [{
            "role": "system",
            "content": system_prompt
        }]
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
        self.history.append({
            "role": "assistant",
            "content": str(response.choices[0].message.content)
             }
        )

        return json_text_answer

    def configure(self):
        load_dotenv()

    def to_string(self):
        return "DeepSeek"
