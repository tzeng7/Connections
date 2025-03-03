import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from Game import Game


# TODO: how to find out whether answer was correct
class Connections:
    def __init__(self):
        self.service = webdriver.Chrome()
        self.wait = WebDriverWait(self.service, timeout=2)
        self.game = Game(set())
        self.correct = 0
        self.answers = [{'LOAF', 'LOUNGE', 'CHILL', 'REST'}, {'SCROLL', 'ROLL', 'REEL', 'BOLT'}, {'BAR', 'COIN', 'LEAF', 'NUGGET'}, {'BONE', 'DINOSAUR', 'CLUB', 'RUBBLE'}]
        self.index = 0

    def has_ended(self):
        try:
            congrats_text = self.service.find_element(By.CLASS_NAME, "Congrats-module_modalTitle__QDY5W")
            return congrats_text.is_displayed()
        except NoSuchElementException as e:
            print(e.msg)
            return False

    def click_element_by_class_name(self, class_name):
        try:
            button = self.service.find_element(By.CLASS_NAME, class_name)
            self.wait.until(lambda _: button.is_displayed())
            button.click()
        except NoSuchElementException as e:
            print(e.msg)
            return

    def click_element_by_xpath(self, path):
        try:
            card = self.service.find_element(By.XPATH, path)
            self.wait.until(lambda _: EC.element_to_be_clickable(card))
            print(f'{path} + {card.is_displayed()}')
            card.click()
            return card
        except NoSuchElementException as e:
            print(e)
            return
        except InvalidSelectorException as e:
            print(e)
            return

    def find_num_correct_themes(self):
        try:
            ol = self.service.find_element(By.CLASS_NAME, "SolvedCategories-module_solvedCategoriesContainer___8Udu")
            solved = ol.find_elements(By.CLASS_NAME, "SolvedCategory-module_solvedCategory___8phN")
            return len(solved)
        except NoSuchElementException as e:
            return 0

    def shows_one_off(self):
        try:
            one_off = self.service.find_element(By.CLASS_NAME, "Toast-module_toast__YAoDa")
            return one_off.is_displayed()
        except NoSuchElementException as e:
            print(e.msg)
            return False

    def shows_correct(self):
        new_correct = self.find_num_correct_themes()
        print(f'{self.correct} {new_correct}')
        if self.correct < new_correct:
            self.correct = new_correct
            return True
        return False
        # update game words list

    def setup(self):
        self.service.get("https://www.nytimes.com/games/connections")

        # progression: terms -> play -> play game
        self.click_element_by_class_name("purr-blocker-card__button")
        self.click_element_by_class_name("pz-moment__button")

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Card-module_label__U_Q2H")))
        cards = self.service.find_elements(By.CLASS_NAME, "Card-module_label__U_Q2H")
        card_texts = [card.text for card in cards]
        self.game.words = card_texts

    def reset(self, guesses):
        for guess in guesses:
            path = f"//label[@data-flip-id='{guess}']"
            self.click_element_by_xpath(path)
            time.sleep(1)

    def make_guess(self, prompt):
        guesses = self.game.make_guess(prompt)
        for guess in guesses:
            path = f"//label[@data-flip-id='{guess}']"
            self.click_element_by_xpath(path)
            time.sleep(.5)
        self.click_element_by_xpath("//button[@data-testid='submit-btn']")
        return guesses
    # def make_guess(self, prompt):
    #     guesses = self.answers[self.index]
    #     self.index += 1
    #     print(guesses)
    #     for guess in guesses:
    #         path = f"//label[@data-flip-id='{guess}']"
    #         card = self.click_element_by_xpath(path)
    #         time.sleep(.5)
    #     self.click_element_by_xpath("//button[@data-testid='submit-btn']")
    #     return guesses


    def play(self):
        self.setup()
        prompt = open("prompt.txt").read()
        prompt += f'\nInput: {list(self.game.words)}'
        while not self.has_ended():
            time.sleep(1)
            # make guess --> check if one off or correct --> update prompt
            answer = self.make_guess(prompt)
            time.sleep(2)
            if answer not in self.game.guesses:
                if self.shows_correct():
                    self.game.remove_guess_from_words(answer)
                    prompt = f'''That is correct.
                             \nNow there are {len(self.game.words)} words remaining. Pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                             \nInput: {list(self.game.words)}
                             \nSolution:
                             '''
                elif self.shows_one_off():
                    print(f'{answer} is almost correct.')
                    prompt = f'''That is incorrect.
                             \n3 of the words in the guess are correctly matched.
                             \nPlease pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                             \nInput: {list(self.game.words)}
                             \nSolution:
                             '''
                    time.sleep(2)
                    self.click_element_by_xpath("//button[@data-testid='deselect-btn']")
                else:
                    print(f'{answer} is incorrect.')
                    prompt = f'''That is incorrect.
                             \nPlease pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                             \nInput: {list(self.game.words)}
                             \nSolution:
                             '''
                    time.sleep(2)
                    self.click_element_by_xpath("//button[@data-testid='deselect-btn']")
            else:
                prompt = f'''You have tried this combination before. Pick a different combination of four words that share a common theme. Return a json object with keys "answer" and "reason"
                        \nInput: {list(self.game.words)}
                        \nSolution:
                        '''
                time.sleep(2)
                self.click_element_by_xpath("//button[@data-testid='deselect-btn']")
            self.game.add_guess(answer)
            self.service.implicitly_wait(5)


Connections().play()
