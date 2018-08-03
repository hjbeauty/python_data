import requests
import bs4
import pathlib
import telegram
from selenium import webdriver

class Company():
    def __init__(self, name, description, position, salary, logo_src):
        self.name = name
        self.description = description
        self.position = position
        self.salary = salary
        self.logo_src = logo_src

    @classmethod
    def from_html(cls, html_src):
        pass

    def __str__(self):
        return '회사명: {} 직무: {}'.format(self.name, self.position)


def initialize_bot():
    with open("../../datas/telegramToken.txt", "r") as f:
        user = f.readline().strip('\n')
        token = f.readline().strip('\n')
        print(token)

    bot = telegram.Bot(token)
    print(bot)

if __name__ == "__main__":
    initialize_bot()
    url = 'https://www.rocketpunch.com/jobs?career_type=1&job=sw-developer&location=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&page=1&specialty=Java&specialty=Python'
    driver = webdriver.Chrome('C:\\Users\\kmh45\\Documents\\Programming\\python\\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get('https://www.rocketpunch.com/jobs?career_type=1&job=sw-developer&location=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&page=1&specialty=Java&specialty=Python')

    #profile = driver.find_element_by_xpath('//*[@id="company-list"]/div[3]/div[2]/div[7]/div[5]/div/a').click()
    html = driver.page_source
    bs = bs4.BeautifulSoup(html, 'html.parser')
