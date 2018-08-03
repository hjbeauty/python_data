import requests
import bs4
import pathlib
import telegram
from selenium import webdriver
import time

class Company():
    def __init__(self, name, description, position, salary, url):
        self.name = name
        self.description = description
        self.position = position
        self.salary = salary
        #self.logo_src = logo_src
        self.url = url

    @classmethod
    def from_html(cls, html_src):
        name = html_src.find('h4', class_='header').strong.get_text().strip()
        description = html_src.find('div', class_='description').get_text().strip()
        position = html_src.find('a', class_='job-title').get_text().strip()
        salary = html_src.find('span', class_='job-stat-info').get_text().strip()
        #logo_src = html_src.find('div', class_='logo').a.div.img['src'].strip()
        url = html_src.find('div', class_='company-jobs-detail').div.a['href'].strip()
        return cls(name, description, position, salary, url)

    def __str__(self):
        return '회사명: {} 직무: {}'.format(self.name, self.position)

    def notice_info(self, user, bot):
        #bot.send_photo(user, self.logo_src)
        time.sleep(5)
        bot.send_message(user, self.name + ' - ' + self.description + '\n' + \
                        self.position + ' ' + self.salary + '\n link: https://www.rocketpunch.com' + self.url)
        time.sleep(5)

def initialize_bot():
    with open("../../datas/telegramToken.txt", "r") as f:
        user = f.readline().strip('\n')
        token = f.readline().strip('\n')
        print(token)

    bot = telegram.Bot(token)
    print(bot)
    return user, bot

if __name__ == "__main__":
    user, bot = initialize_bot()
    url = 'https://www.rocketpunch.com/jobs?career_type=1&job=sw-developer&location=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&page=1&specialty=Java&specialty=Python'
    driver = webdriver.Chrome('C:\\Users\\kmh45\\Documents\\Programming\\python\\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get(url)

    #profile = driver.find_element_by_xpath('//*[@id="company-list"]/div[3]/div[2]/div[7]/div[5]/div/a').click()
    html = driver.page_source
    bs = bs4.BeautifulSoup(html, 'html.parser')
    company_list = bs.find('div', id = 'company-list')
    companys = company_list.find_all('div', class_='company')
    
    company_instances = list()
    for company in companys:
        company_instances.append(Company.from_html(company))
    
    for company in company_instances:
        company.notice_info(user, bot)