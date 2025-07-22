import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from models.ChatGPTAPI import ChatGPTLLMPrompter
from models.GeminiAPI import GeminiLLMPrompter
from models.ClaudeAPI import ClaudeLLMPrompter
from models.DeepseekAPI import DeepseekLLMPrompter
from Game import Game
from StatWriter import StatWriter
import multiprocessing

class GameAutomationStatCollector():
    def __init__(self, model):
        
        chrome_options = Options()
        # Add uBlock Origin extension for ad blocking
        chrome_options.add_extension("./ublock.crx")
        chrome_options.add_argument("--block-new-web-contents")  # Block popups

        
        # # Additional options to improve ad blocking and performance
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument("--disable-web-security")
        # chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        # chrome_options.add_argument("--disable-extensions-except=./ublock.crx")
        # chrome_options.add_argument("--load-extension=./ublock.crx")
        
        self.service = webdriver.Chrome(options=chrome_options)
        # Execute script to hide webdriver property
        self.service.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.service, timeout=1.5)
        self.game = Game(set(), prompter=model())
        self.correct = 0
        self.index = 0
        
        # Initialize stat tracking
        self.stat_writer = StatWriter("connections_stats.csv")
        
    def click_element_by_class_name(self, class_name):
        try:
            # button = self.service.find_element(By.CLASS_NAME, class_name)
            # self.wait.until(lambda _: EC.element_to_be_clickable(button))
            button = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            self.wait.until(EC.visibility_of(button))
            self.wait.until(EC.element_to_be_clickable(button))
            button.click()
        except TimeoutException as e:
            print(f"Timeout waiting for element: {e}")
            return
        except NoSuchElementException as e:
            print(e.msg)
            return
        except InvalidSelectorException as e:
            print(e)
            return

    def click_element_by_xpath(self, path):
        try:
            card = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path)))
            print(card)
            self.wait.until(EC.visibility_of(card))
            self.wait.until(EC.element_to_be_clickable(card))
            card.click()
            return card
        except TimeoutException as e:
            print(f"Timeout waiting for element: {e}")
            return
        except NoSuchElementException as e:
            print(e)
            return
        except InvalidSelectorException as e:
            print(e)
            return


#
    def setup(self, number):
        
        self.service.get(f"https://connectionsplus.io/game/{number}")
        
        self.game.reset_game_state()
        self.wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "css-butdwn")))
        cards = self.service.find_elements(
            By.CLASS_NAME, "css-butdwn")

        # get card texts for the input array
        card_texts = [card.text for card in cards]
        self.game.words = card_texts

    def make_guess(self, prompt):
        guesses = self.game.make_guess(prompt)
        for guess in guesses:
            path = f"//button[.//p[text()='{guess}']]"
            self.click_element_by_xpath(path)
            time.sleep(.5)
        self.click_element_by_xpath("//button[text()='Submit']")
        time.sleep(1)
        return guesses
    
    def find_num_correct_themes(self):
        print("Testing if correct")
        try:
            # ol = self.service.find_element(
            #     By.CLASS_NAME, "SolvedCategories-module_solvedCategoriesContainer___8Udu")
            solved = self.service.find_elements(
                By.CLASS_NAME, "css-jtgcyt")
            return len(solved)
        except NoSuchElementException as e:
            return 0

    def shows_one_off(self):
        print("Testing one off")
        try:
            self.service.implicitly_wait(2)
            one_off = self.service.find_element(
                By.CLASS_NAME, "chakra-alert__desc")
            if one_off.is_displayed():
                return one_off.text == "One away..."
                #input here
            return False
        except NoSuchElementException as e:
            return False
        except TimeoutException as e:
            return False

    def shows_correct(self):
        new_correct = self.find_num_correct_themes()
        if self.correct < new_correct:
            self.correct = new_correct
            return True
        return False
    
    def has_ended_incorrect(self):
        print("Ended Incorrect")
        try:
            self.service.implicitly_wait(2)
            incorrect = self.service.find_element(By.CLASS_NAME, "chakra-modal__header")
            return incorrect.text == "Almost there!"
            return False
        except NoSuchElementException as e:
            return False
        except TimeoutException as e:
            return False
    
    def play(self, num):
        # Reset game state for new game
        self.game.reset_game_state()
        self.correct = 0
        
        self.setup(num)
        prompt = open("prompt.txt").read()
        prompt += f'\nInput: {list(self.game.words)}'
        while self.game.incorrect < 4 and self.correct < 4:
            if self.game.incorrect == 2:
                self.game.switch_model()
            time.sleep(1)

            # make guess --> check if one off or correct --> update prompt
            answer = self.make_guess(prompt)
            if answer not in self.game.guesses:
                time.sleep(1)
                # check one away first due to time-sensitive one away messaging
                if self.shows_one_off():
                    self.game.increment_incorrect()
                    print(f'{answer} is almost correct.')
                    prompt = f'''That is incorrect.
                             \n3 of the words in the guess are correctly matched.
                             \nPlease pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                             \nInput: {list(self.game.words)}
                             \nSolution:
                             '''
                    time.sleep(.5)
                    self.click_element_by_xpath(
                        "//button[text()='Deselect All']")
                elif self.has_ended_incorrect():
                    break
                elif self.shows_correct():
                    self.game.remove_guess_from_words(answer)
                    print(f'{answer} is correct.')
                    prompt = f'''That is correct.
                             \nNow there are {len(self.game.words)} words remaining. Pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                             \nInput: {list(self.game.words)}
                             \nSolution:
                             '''
                else:
                    self.game.increment_incorrect()

                    print(f'{answer} is incorrect.')
                    prompt = f'''That is incorrect.
                             \nPlease pick 4 words that share a common theme. Return a json object with keys "answer" and "reason"
                             \nInput: {list(self.game.words)}
                             \nSolution:
                             '''
                    self.click_element_by_xpath(
                        "//button[text()='Deselect All']")
            else:
                prompt = f'''You have tried this combination before. Pick a different combination of four words that share a common theme. Return a json object with keys "answer" and "reason"
                        \nInput: {list(self.game.words)}
                        \nSolution:
                        '''
                time.sleep(1)
                self.click_element_by_xpath(
                    "//button[text()='Deselect All']")
            self.game.add_guess(answer)
        time.sleep(6.5)
        print(f"Game has ended.")
        
        # Determine game outcome and write stats
        game_outcome = "won" if self.correct >= 4 else "lost"
        model_name = self.game.prompter.to_string()
        self.stat_writer.write_game_stats(model_name, self.game.guesses, game_outcome)
        
def run(m):
    automated_connections_run = GameAutomationStatCollector(m)
    for i in range(4, 51):
        automated_connections_run.play(i)
run(DeepseekLLMPrompter)
