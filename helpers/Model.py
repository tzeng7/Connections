from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def prompt_llm(self, input_prompt: str):
        pass

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def swap_model(self):
        pass

    @abstractmethod
    def to_string(self):
        pass
