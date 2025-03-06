from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def prompt_llm(self, input_prompt: str):
        pass

    @abstractmethod
    def configure(self):
        pass
