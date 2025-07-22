
from helpers.Answer import Answer
from helpers.Model import Model


SOLUTION_LENGTH = 4


class Game:

    def __init__(self, words: set[str], prompter: Model):
        self.words = words
        self.guesses = []
        self.incorrect = 0
        self.prompter = prompter

    def run_prompt(self, prompt: str) -> Answer:
        answer = self.prompter.prompt_llm(prompt)
        print(answer.reason)
        return answer

    def remove_guess_from_words(self, guess: set[str]):
        for word in guess:
            self.words.remove(word)

    def add_guess(self, guess):
        self.guesses.append(guess)

    def make_guess(self, prompt: str):
        answer = set(self.run_prompt(prompt).answer)
        print(answer)
        return answer

    def increment_incorrect(self):
        self.incorrect = self.incorrect + 1

    def switch_model(self):
        self.prompter.swap_model()
    
    def reset_game_state(self):
        """Reset game state for a new game"""
        self.words = set()
        self.guesses = []
        self.incorrect = 0
