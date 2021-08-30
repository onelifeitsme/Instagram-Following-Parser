from selenium import webdriver
from time import sleep
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'accept': '*/*'}

print("Введите ссылку на профиль")
product = str(input())
login = 'onelifeitsme'
password = 'OneLife2019'

driver = webdriver.Chrome()

driver.get(product)

sleep(1)

def sign_ing(login, password):
    login = 'onelifeitsme'
    pasword = 'OneLife2019'
    login_field = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    login_field.send_keys(login)
    password_field = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    password_field.send_keys(pasword)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
    sleep(4)

driver.get('https://www.instagram.com/')
sign_ing(login, password)
driver.get(product)
driver.find_element_by_xpath('//li[3]/a').click()
sleep(3)

actions = ActionChains(driver)
actions.send_keys(Keys.TAB * 6)
actions.perform()
sleep(1)
actions = ActionChains(driver)
actions.send_keys(Keys.END)
actions.perform()
sleep(1)
actions = ActionChains(driver)
actions.send_keys(Keys.TAB * 6)
actions.perform()
sleep(1)
actions = ActionChains(driver)
actions.send_keys(Keys.END)
for i in range(40):
    actions.perform()
    sleep(0.5)




sleep(3)

accounts = []
users = driver.find_elements_by_xpath('/html/body/div[6]/div/div/div[3]/ul/div/li/div/div[1]/div[2]/div[1]/span/a')
if users:
    print("eee")
else:
    print('noo')
for i in users:
    accounts.append('https://www.instagram.com/' + i.text)

base = []


def parse_account_info(account):
    try:
        close_or_not = driver.find_element_by_xpath('//div[1]/div/h2').text
    except:
        close_or_not = 'открытый'
    if "закрытый аккаунт" in close_or_not:
        try:
            name = driver.find_element_by_xpath('//div[2]/h1').text
        except:
            name = ' '
        post_number = driver.find_element_by_xpath('//li[1]/span/span').text
        followers_number = driver.find_element_by_xpath('//li[2]/span/span').text
        following_number = driver.find_element_by_xpath('//li[3]/span/span').text
        try:
            bio = driver.find_element_by_xpath('//div[2]/span').text
        except:
            bio = ' '
        try:
            link = driver.find_element_by_xpath('//div/div[1]/a').text
            if 'подписан' in link:
                link = ' '
        except:
            link = ' '
        category = ' '


    else:
        try:
            name = driver.find_element_by_xpath('//div[2]/h1').text
        except:
            name = ' '
        try:
            post_number = driver.find_element_by_xpath('//li[1]/span/span').text
        except:
            post_number = ' '
        try:
            followers_number = driver.find_element_by_xpath('//li[2]/a/span').text
        except:
            followers_number = ' '
        try:
            following_number = driver.find_element_by_xpath('//li[3]/a/span').text
        except:
            following_number = ' '
        try:
            category = driver.find_element_by_xpath('//header/section/div[2]/div/span').text
        except:
            category = ' '
        try:
            bio = driver.find_element_by_xpath('//div[2]/span').text
        except:
            bio = ' '
        try:
            link = driver.find_element_by_xpath('//header/section/div[2]/a').text
            if 'подписан' in link:
                link = ' '
        except:
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


account_number = 0
for i in accounts:
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
    account_number +=1
    print(account_number)

with open("insta.csv", "w", encoding='utf-8') as temp:
    polya = ['Аккаунт', 'Имя', 'Категория', 'Постов', 'Подписчиков', 'Подписок', 'БИО', 'Ссылка в био']
    out = csv.DictWriter(temp, fieldnames=polya)
    out.writeheader()
    for i in base:
        out.writerow(i)
















