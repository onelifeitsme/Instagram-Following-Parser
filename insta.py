from selenium import webdriver
from time import sleep
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.131 Safari/537.36', 'accept': '*/*'}
mobile_emulation = {"deviceName": "Nexus 5"}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

print("Введите ссылку на профиль")
product = str(input())
login = 'ВАШ ЛОГИН'
password = 'ВАШ ПАРОЛЬ'

driver = webdriver.Chrome(options=chrome_options)
# ЕСЛИ ВЫ НА ЛИНУКСЕ, ТО НУЖНО ИСПОЛЬЗОВАТЬ ВАРИАНТ НИЖЕ
# driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

sleep(1)


def sign_ing(login, password):
    """Функция аутентификации"""
    sleep(3)
    login_field = driver.find_element(By.XPATH, '//input[@name="username"]')
    login_field.send_keys(login)
    password_field = driver.find_element(By.XPATH, '//input[@name="password"]')
    password_field.send_keys(password)
    driver.find_element(By.XPATH, '//div[text()="Войти"]').click()
    sleep(4)


driver.get('https://www.instagram.com/')

sleep(3)
# КЛИК ПО КНОПКЕ ЛОГИН
driver.find_element(By.XPATH, '//div[3]/button[1]').click()

# ПРОЦЕСС АВТОРИЗАЦИИ
sign_ing(login, password)
driver.get(product)
sleep(7)

# КЛИК ПО КНОПКЕ ПОДПИСКИ
following_number = int(driver.find_element(By.XPATH, '//main/div/ul/li[3]/a/span').text)
driver.find_element(By.XPATH, '//a[contains(@href,"following")]').click()


sleep(3)


def scroll():
    """Функция скролла"""
    for i in range(round(following_number/12)):
        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN)
        actions.perform()
        sleep(1)
        actions = ActionChains(driver)
        actions.send_keys(Keys.END)
        actions.perform()
        sleep(1)


scroll()

# ПОЛУЧЕНИЕ СПИСКА ПОДПИСОК
users = driver.find_elements(By.XPATH, '//li/div/div[1]/div[2]/div[1]/a')
print('Получено ', len(users), ' аккаунтов')
accounts = ['https://www.instagram.com/' + user.text for user in users]

base = []


def parse_account_info(account):
    """ФУНКЦИЯ ПАРСИНГА ИНФЫ ВСЕХ ПОЛЕЙ В АККАУНТЕ"""
    try:
        close_or_not = driver.find_element(By.XPATH, '//div[1]/div/h2').text
    except NoSuchElementException:
        close_or_not = 'открытый'
    if "закрытый аккаунт" in close_or_not:
        try:
            name = driver.find_element(By.XPATH, '//main/div/div[1]/h1').text
        except NoSuchElementException:
            name = ' '
        post_number = driver.find_element(By.XPATH, '//main/div/ul/li[1]/span/span').text
        followers_number = driver.find_element(By.XPATH, '//main/div/ul/li[2]/a/span').text
        following_number = driver.find_element(By.XPATH, '//main/div/ul/li[3]/a/span').text
        try:
            bio = driver.find_element(By.XPATH, '//main/div/div[1]/span').text
        except NoSuchElementException:
            bio = ' '
        try:
            link = driver.find_element(By.XPATH, '//main/div/div[1]/a').text
            if 'подписан' in link or 'follow' in link:
                link = ' '
        except NoSuchElementException:
            link = ' '
        category = ' '

    else:
        try:
            name = driver.find_element(By.XPATH, '//main/div/div[1]/h1').text
        except NoSuchElementException:
            name = ' '
        try:
            post_number = driver.find_element(By.XPATH, '//li[1]/span/span').text
        except NoSuchElementException:
            post_number = ' '
        try:
            followers_number = driver.find_element(By.XPATH, '//li[2]/a/span').text
        except NoSuchElementException:
            followers_number = ' '
        try:
            following_number = driver.find_element(By.XPATH, '//li[3]/a/span').text
        except NoSuchElementException:
            following_number = ' '
        try:
            category = driver.find_element(By.XPATH, '//main/div/div[1]/div/span').text
        except NoSuchElementException:
            category = ' '
        try:
            bio = driver.find_element(By.XPATH, '//main/div/div[1]/span').text
        except NoSuchElementException:
            bio = ' '
        try:
            link = driver.find_element(By.XPATH, '//main/div/div[1]/a').text
            if 'подписан' in link or 'follow' in link:
                link = ' '
        except NoSuchElementException:
            link = ' '

    base.append({
        'Аккаунт': account,
        'Имя': name,
        'Категория': category,
        'Постов': post_number,
        'Подписчиков': followers_number,
        'Подписок': following_number,
        'БИО': bio,
        'Ссылка в био': link,

    })


# ПРОХОД ПО КАЖДОМУ АККАУНТУ, ПАРСИНГ И ЗАПИСЬ ИНФЫ В СПИСОК СЛОВАРЕЙ base
account_number = 0
for acc in accounts:
    try:
        driver.get(accounts[account_number])
    except:
        pass
    sleep(2)
    try:
        parse_account_info(accounts[account_number])
    except:
        pass
    sleep(2)
    account_number += 1
    print(account_number)


# СОЗДАНИЕ ФАЙЛА И ЗАПИСЬ К НЕГО ИТОГА ПАРСИНГА
with open("insta.csv", "w", encoding='utf-8') as temp:
    polya = ['Аккаунт', 'Имя', 'Категория', 'Постов', 'Подписчиков', 'Подписок', 'БИО', 'Ссылка в био']
    out = csv.DictWriter(temp, fieldnames=polya)
    out.writeheader()
    for i in base:
        out.writerow(i)
