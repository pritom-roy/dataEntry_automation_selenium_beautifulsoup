import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7"
}

response = requests.get(
    url="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D",
    headers=header)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "html.parser")

price = soup.find_all('span', {'data-test': "property-card-price"})
price_list = []
for money in price:
    price_list.append(money.text)

address = soup.find_all('address', {'data-test': "property-card-addr"})
address_list = []

for location in address:
    address_list.append(location.text)

pagelink = soup.find_all('a', {'data-test': "property-card-link"})
pagelink_list = []

for link in pagelink:
    href = link["href"]

    if "https" in href:
        pagelink_list.append(href)
    else:
        pagelink_list.append(f"https://www.zillow.com/b/{href}")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
url = Service('Your Driver Link')

driver = webdriver.Chrome(options=chrome_options, service=url)
form_url = "Your form link"


driver.get(url=form_url)


for i in range(len(price_list)):
    time.sleep(2)

    address = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(address_list[i])

    cost = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(2)
    cost.send_keys(price_list[i])

    links = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(2)
    links.send_keys(pagelink_list[i])

    time.sleep(1)
    submit = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit.click()

    time.sleep(2)
    again = driver.find_element(by='xpath', value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    again.click()

driver.quit()