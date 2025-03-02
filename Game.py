import time

from GeminiAPI import LLMPrompter, Answer
from Solution import Solution
import json
import re

SOLUTION_LENGTH = 4


class Game:

    def __init__(self, words: set[str]):
        self.words = words
        self.solutions = Solution([{"GNASH", "GRATE", "GRIND", "SCRAPE"},
                        {"CAN", "FERMENT", "FREEZE", "PICKLE"},
                        {"BUTTER", "HOT SAUCE", "JAM", "SYRUP"},
                        {"BEANS", "GUTS", "MILK", "TEA"}])
        self.guesses = []
        self.prompter = LLMPrompter()

    def set_words(self, image_path):
        self.words = self.prompter.read_image(image_path)
    def run_prompt(self, prompt: str) -> Answer:
        answer = self.prompter.prompt_llm(prompt)
        return answer

    def validate(self, result: set[str]):
        max_same = 0
        for solution in self.solutions.get_solutions():
            count = 0
            for word in result:
                if word in solution:
                    count += 1
            max_same = max(count, max_same)
        return max_same

    # TODO: clean up code, figure out why it keeps coming up with solutions with words that are already used
    # TODO: at 4 words left in the set, just return those words
    def play(self):
        self.set_words("images/test2.png")
        has_switched = False
        max_count = 10
        count = 0
        prompt = open("prompt.txt").read()
        prompt += f'\nInput: {list(self.words)}'
        while self.words:
            answer = set(self.run_prompt(prompt).answer)

            if count >= max_count and not has_switched:
                # swap to pro model if flash model gets it wrong too many times
                self.prompter.swap_model()
                has_switched = True

            if answer not in self.guesses:
                self.guesses.append(answer)
                check_answer = self.validate(answer)

                ### correct answer
                if check_answer == SOLUTION_LENGTH:

                    ### switch back to flash model if pro model gets it right
                    if not self.prompter.uses_flash and count >= max_count:
                        self.prompter.swap_model()
                        has_switched = False
                        count = 0

                    print(f'{answer} is correct.')
                    for word in answer:
                        self.words.remove(word)
                    prompt = f'''That is correct.
                              \nNow there are {len(self.words)} words remaining. Pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                              \nInput: {list(self.words)}
                              \nSolution: 
                              '''
                # off by one
                elif check_answer == 3:
                    print(f'{answer} is almost correct.')
                    prompt = f'''That is incorrect. 
                             \n3 of the words in the guess are correctly matched.
                             \nPlease pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                             \nInput: {list(self.words)}
                             \nSolution:
                             '''
                # off by two or more
                else:
                    print(f'{answer} is incorrect.')
                    prompt = f'''That is incorrect. 
                            \nPlease pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                            \nInput: {list(self.words)}
                            \nSolution:
                             '''
            else:
                prompt = f'''You have tried this combination before. Pick a different combination of four words that share a common theme. Return a json object with keys "answer" and "reason"
                        \nInput: {list(self.words)}
                        \nSolution:
                        '''
            count += 1

            if len(self.words) == 0:
                print("Game won.")


# list_test = ["SAXOPHONE", "ROLLERBLADE", "PACIFIER", "SKETCH", "RATTLESNAKE", "MONOLOGUE", "CERTIFICATE", "TITLE", "RECEIPT", "SKATEBOARD", "SONG", "DONUT", "DEED", "DANCE", "SHAKESPEARE", "ANDROID"]
# test = set(list_test)
Game(set()).play()


