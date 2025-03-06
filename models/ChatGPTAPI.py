import re
import json

from dotenv import load_dotenv
import os
from pydantic import BaseModel
from openai.types.chat import ChatCompletionMessageParam

from helpers.Answer import Answer
from helpers.Model import Model
from openai import OpenAI


class ChatGPTLLMPrompter(Model):

    def __init__(self):
        self.configure()
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        self.chat_session = None
        self.history = []

    def swap_model(self):
        pass

    def prompt_llm(self, input_prompt: str):
        self.history.append({
            "role": "user",
            "content": input_prompt
        })
        self.chat_session = self.client.chat.completions.create(
            messages=self.history,
            model="gpt-4o-mini",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "guess",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "reason": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        )
        response = self.chat_session.choices[0].message.content

        json_text_answer = Answer(**json.loads(response))

        self.history.append({
            "role": "assistant",
            "content": response
        })

        return json_text_answer

    def configure(self):
        load_dotenv()
        return os.getenv("OPENAI_KEY")


prompt = open("prompt.txt").read()
print(ChatGPTLLMPrompter().prompt_llm(prompt))
