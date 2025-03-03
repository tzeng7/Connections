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
            card.click()
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

    def setup(self):
        self.service.get("https://www.nytimes.com/games/connections")

        # progression: terms -> play -> play game
        self.click_element_by_class_name("purr-blocker-card__button")
        self.click_element_by_class_name("pz-moment__button")

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Card-module_label__U_Q2H")))
        cards = self.service.find_elements(By.CLASS_NAME, "Card-module_label__U_Q2H")
        card_texts = [card.text for card in cards]
        self.game.set_words(card_texts)

    def reset(self, guesses):
        for guess in guesses:
            path = f"//label[@data-flip-id='{guess}']"
            self.click_element_by_xpath(path)
            time.sleep(1)

    def make_guess(self):
        guesses = self.game.make_guess()
        for guess in guesses:
            path = f"//label[@data-flip-id='{guess}']"
            self.click_element_by_xpath(path)
            time.sleep(1)
        self.click_element_by_xpath("//button[@data-testid='submit-btn']")
        time.sleep(1)
        self.click_element_by_xpath("//button[@data-testid='deselect-btn']")


    def play(self):
        self.setup()
        while not self.has_ended():
            self.make_guess()


Connections().play()
