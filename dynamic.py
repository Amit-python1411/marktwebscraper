from bs4 import BeautifulSoup
import requests
import re
import pandas
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import common

# Opening a webpage with options
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(options=chromeOptions)

driver.get("https://www.mediamarkt.se")
action = ActionChains(driver)

media_drop_down = driver.find_element_by_xpath("//*[@id='rise-header']/div[1]/nav[2]/div[1]/ul/li[1]")
action.move_to_element(media_drop_down).perform()
time.sleep(2)
media_drop = driver.find_element_by_xpath("//*[@id='rise-header']/div[1]/nav[2]/div[1]/ul/li[1]/div/ul/li[5]/a")
action.move_to_element(media_drop).perform()
media_drop.click()
time.sleep(2)

media_ele = driver.find_element_by_link_text("Alla TV-apparater").click()
#element = WebDriverWait(driver, 10).until(
#   ec.element_to_be_clickable((By.LINK_TEXT, "Alla TV-apparater")))
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)
# search_ele = driver.find_elements_by_xpath("//div[@class='inline-input five-digits']")
# tum = search_ele[2].find_element_by_class_name(
#     'price-from'
# )

tum = driver.find_element_by_xpath("//*[@id='filters']/form/fieldset[8]/div[2]/div[2]/input")
tum.clear()
driver.implicitly_wait(10)
tum.send_keys("55")

tum_to = driver.find_element_by_xpath("//*[@id='filters']/form/fieldset[8]/div[2]/div[4]/input")
tum_to.clear()
tum_to.send_keys("65")
tum_to.send_keys(Keys.RETURN)
time.sleep(6)

price = driver.find_element_by_xpath("//*[@id='filters']/form/fieldset[5]/div[2]/div[2]/input")
price.clear()
price.send_keys("8000")

price_to = driver.find_element_by_xpath("//*[@id='filters']/form/fieldset[5]/div[2]/div[4]/input")
price_to.clear()
price_to.send_keys("50000")
price_to.send_keys(Keys.RETURN)

time.sleep(6)
files = []
page_source = driver.page_source
files.append(page_source)

status = True
while status:
    try:
        next_page = driver.find_element_by_xpath("//*[@id='category']/div[2]/ul/li[3]/a")
        next_page.click()
        page_source = driver.page_source
        files.append(page_source)
        time.sleep(2)
    except common.exceptions.ElementClickInterceptedException:
        break

print(len(files))
#next_page = WebDriverWait(driver, 10).until(
#   ec.element_to_be_clickable((By.XPATH, "//*[@id='category']/div[2]/ul/li[3]/a")))

names = []
brands = []
prices = []
dimensions = []

for file in files:
    soup = BeautifulSoup(file, 'lxml')
# print(soup.prettify())
    rows = soup.find_all('script')
    for row in rows:
        if "var product" in row.text:
            #m = re.compile('<script>(.*?)</script>', re.DOTALL).findall(row.text)
            m = re.search('{(.+?)}', row.string)
            #print(m.group(1))
            splittext = m.group(1).split(',')
            for n in splittext:
                if "name" in n:
                    split_name = n.split(':')
                    names.append(split_name[1].strip('\"'))
                if "price" in n:
                    split_price = n.split(':')
                    prices.append(split_price[1].strip('\"'))
                if "dimension10" in n:
                    dimensions.append(n)
                if "brand" in n:
                    split_brand = n.split(':')
                    brands.append(split_brand[1].strip('\"'))


cols = ['Name', 'Brand', 'Price']
export = pandas.DataFrame({'Name': names,
                           'Brand': brands,
                           'Price': prices,
                           })[cols]

export.to_excel('mediamarkt_'+str(date.today())+'.xls')

driver.quit()




