import pytest
from settings import email, password
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(r'C:\Users\Admin\Desktop\chromedriver.exe')
   pytest.driver.get('https://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

@pytest.fixture()
def go_to_my_pets():

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
   pytest.driver.find_element('id', "email").send_keys(email)

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
   pytest.driver.find_element('id',"pass").send_keys(password)

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
   pytest.driver.find_element('css selector', "button[type='submit']").click()

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
