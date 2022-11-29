import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from settings import email, password


def test_1_all_pets_are_present(go_to_my_pets):
   '''Проверяем, что на странице со списком моих питомцев присутствуют все питомцы'''

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))

   statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

   pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])
   number_of_pets = len(pets)

   assert number == number_of_pets


def test_2_half_has_photo(go_to_my_pets):
   '''Проверяем, что на странице со списком моих питомцев хотя бы у половины питомцев есть фото'''

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))

   statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])

   half = number // 2

   number_а_photos = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         number_а_photos += 1

   assert number_а_photos >= half
   print(f'количество фото: {number_а_photos}')
   print(f'Половина от числа питомцев: {half}')


def test_3_pets_have_NameAgeBreed(go_to_my_pets):
   '''Проверяем, что на странице со списком моих питомцев, у всех питомцев есть имя, возраст и порода'''

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
   # и разделяем по пробелу. Находим количество элементов в получившемся списке и сравниваем их
   # с ожидаемым результатом
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      result = len(split_data_pet)
      assert result == 3


def test_4_pets_have_different_names(go_to_my_pets):
   '''Проверяем, что на странице со списком моих питомцев у всех питомцев разные имена'''

   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   pets_name = []
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      pets_name.append(split_data_pet[0])

   # Перебираем имена и, если имя повторяется, то прибавляем к счётчику r единицу.
   # Проверяем если r == 0, то повторяющихся имён нет.
   r = 0
   for i in range(len(pets_name)):
      if pets_name.count(pets_name[i]) > 1:
         r += 1
   assert r == 0
   print(r)
   print(pets_name)


def test_no_repeating_pets(go_to_my_pets):
    '''Поверяем что на странице со списком моих питомцев нет повторяющихся питомцев'''

    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    pet_data = pytest.driver.find_elements('css selector','.table.table-hover tbody tr')

    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)

    # Склеиваем имя, возраст и породу, получившиеся склееные слова добавляем в строку
    # и между ними вставляем пробел
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '

    list_line = line.split(' ')

    set_list_line = set(list_line)

    a = len(list_line)
    b = len(set_list_line)
    result = a - b
    assert result == 0


def test_show_my_pets():
   '''Проверяем, что мы оказались на странице "Мои питомцы"'''

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
   pytest.driver.find_element('id', 'email').send_keys(email)

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
   pytest.driver.find_element('id', 'pass').send_keys(password)

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
   pytest.driver.find_element('css selector', 'button[type="submit"]').click()

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'


   #python -m pytest -v --driver Chrome --driver-path C:\Users\Admin\Desktop\chromedriver.exe test_PF.py