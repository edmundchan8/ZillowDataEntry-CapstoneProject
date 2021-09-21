import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
from pprint import pprint
from requests_html import HTMLSession

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22usersSearchTerm%22%3A%2298028%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.31044235385123%2C%22east%22%3A-122.19257964614879%2C%22south%22%3A47.71834069089216%2C%22north%22%3A47.78465876542458%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%2C%22customRegionId%22%3A%22fb39361034X1-CRs2vjk37b9j7i_wmb1d%22%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    "Accept-Language": "en-US"
}
CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"

#google_form = REMOVED FOR PRIVACY PURPOSES

class ZillowScrapper:
    def __init__(self):
        self.response = requests.get(ZILLOW_URL, headers=headers)
        self.contents = self.response.text
        self.soup = BeautifulSoup(self.contents, "html.parser")
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.final_property_links = []
        self.final_property_prices = []
        self.final_property_addresses = []

    def get_links(self):
        property_links_with_duplicates = [link.get('href') for link in self.soup.findAll(name='a', class_="list-card-link")]
        # Remove duplicates
        property_links_removed_dupes = []
        for link in property_links_with_duplicates:
            if link not in property_links_removed_dupes:
                property_links_removed_dupes.append(link)

        # fix the non links
        for link in property_links_removed_dupes:
            if '/b/' in link:
                new_link = f"https://www.zillow.com{link}"
                self.final_property_links.append(new_link)
            else:
                self.final_property_links.append(link)

    def get_prices(self):
        scraped_property_prices = [price.text for price in self.soup.findAll(class_="list-card-price")]
        for price in scraped_property_prices:
            stripped_price = price.split('/', 1)[0]
            stripped_price = stripped_price.split('+', 1)[0]
            self.final_property_prices.append(stripped_price)

    def get_addresses(self):
        self.final_property_addresses = [address.text for address in self.soup.findAll(class_="list-card-addr")]

    def enter_info(self):
        self.driver.get(google_form)
        for prop in range(0, len(self.final_property_prices)):
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                self.final_property_addresses[prop])
            self.driver.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                self.final_property_prices[prop])
            self.driver.find_element_by_xpath(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
                self.final_property_links[prop])
            self.driver.find_element_by_css_selector(".appsMaterialWizButtonPaperbuttonContent").click()
            time.sleep(1)
            # submit new response
            self.driver.find_element_by_css_selector(".freebirdFormviewerViewResponseLinksContainer a").click()

zilScape = ZillowScrapper()
zilScape.get_links()
zilScape.get_prices()
zilScape.get_addresses()
zilScape.enter_info()
