import os
from dotenv import load_dotenv

from helpers.Answer import Answer
from helpers.Model import Model
import anthropic
import json
import re

MAX_TOKENS = 8192

system_prompt = open("system_prompt.txt").read()

class ClaudeLLMPrompter(Model):
    def __init__(self):
        self.configure()
        self.client = anthropic.Anthropic(
            api_key=os.getenv("CLAUDEAI_KEY")
        )
        self.chat_session = None
        self.model = "claude-3-5-haiku-20241022"  # claude-3-7-sonnet-20250219
        self.history = []

    def swap_model(self):
        self.model = "claude-3-7-sonnet-20250219"

    def prompt_llm(self, input_prompt: str):
        self.history.append({
            "role": "user",
            "content": input_prompt
        })

        response = self.client.messages.create(
            model=self.model,
            system=f"Provide exactly one answer without any alternatives or discussing options. "
                   f"Denote the json format starting '```json' and ending with '```' \n {system_prompt}",

            messages=self.history,
            max_tokens=MAX_TOKENS
        )
        text_answer = "".join([block.text for block in response.content if block.type == "text"])
        print(text_answer)
        json_text = re.findall("```json\n((.|\n)*)\n```", text_answer)[0][0]
        # print(json_text)

        json_text_answer = Answer(**json.loads(json_text))

        self.history.append({
            "role": "assistant",
            "content": json_text
        })

        return json_text_answer

    def configure(self):
        load_dotenv()

