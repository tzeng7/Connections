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
            system=system_prompt,
            temperature=0.1,
            messages=self.history,
            max_tokens=MAX_TOKENS
        )
        text_answer = "".join([block.text for block in response.content if block.type == "text"])
        print(text_answer)
        
        # Try to extract JSON from code blocks first
        json_matches = re.findall(r"```json\s*\n?(.*?)\n?\s*```", text_answer, re.DOTALL)
        
        if json_matches:
            # Found JSON in code blocks
            json_text = json_matches[0]
        else:
            # No code blocks found, try to extract raw JSON
            # Look for JSON object pattern starting with { and ending with }
            json_matches = re.findall(r'(\{[^{}]*"answer"[^{}]*"reason"[^{}]*\})', text_answer, re.DOTALL)
            if json_matches:
                json_text = json_matches[0]
            else:
                # Fallback: assume the entire response is JSON
                json_text = text_answer.strip()

        print("Extracted JSON:", json_text)

        json_text_answer = Answer(**json.loads(json_text))

        self.history.append({
            "role": "assistant",
            "content": json_text
        })

        return json_text_answer

    def configure(self):
        load_dotenv()

    def to_string(self):
        return "Claude"

