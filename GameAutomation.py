from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

service = webdriver.Chrome()
service.get("https://www.nytimes.com/games/connections")

wait = WebDriverWait(service, timeout=2)

terms_service = service.find_element(By.CLASS_NAME, "purr-blocker-card__button")
wait.until(lambda _: terms_service.is_displayed())
terms_service.click()
play_button = service.find_element(By.CLASS_NAME, "pz-moment__button")
wait.until(lambda _: play_button.is_displayed())
play_button.click()

wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Card-module_label__U_Q2H")))
cards = service.find_elements(By.CLASS_NAME, "Card-module_label__U_Q2H")
# for card in cards:
#     print(card.text)








