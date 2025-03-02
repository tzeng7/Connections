from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

service = webdriver.Chrome()
service.get("https://www.nytimes.com/games/connections")


terms_service = service.find_element(By.CLASS_NAME, "purr-blocker-card__button")
WebDriverWait(service, timeout=2).until(lambda _: terms_service.is_displayed())
terms_service.click()
play_button = service.find_element(By.CLASS_NAME, "pz-moment__button")
WebDriverWait(service, timeout=5).until(lambda _: play_button.is_displayed())
play_button.click()





