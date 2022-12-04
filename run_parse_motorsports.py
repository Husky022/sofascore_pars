import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from settings import disciplines
from database.manager import DBManager


class WebParser:
    def __init__(self):
        self.driver = self.get_driver()
        self.targets = disciplines
        self.db = DBManager()
        self.parsed_data = []

    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        return webdriver.Chrome(chrome_options=options)

    @staticmethod
    def connect_to_page(driver, target):
        base_url = f'https://www.sofascore.com/{target}'
        try:
            driver.get(base_url)
            driver.implicitly_wait(10)
            return True
        except Exception as e:
            print(e)
            return False

    def parse_html(self, html, category, season):
        soup = BeautifulSoup(html, "html.parser")
        container = soup.find('div', {'class': 'sc-ipEyDJ cQzbjF'})
        events = container.findChildren("a", recursive=False)
        for event in events:
            if season == '2023':
                event_type = 'Not started'
            elif event.find('div', {'class': 'sc-hLBbgP iYSMEZ'}):
                if event.find('div', {'class': 'sc-hLBbgP iYSMEZ'}).find('div', {'class': 'sc-hLBbgP cXmcDo'}):
                    if event.find('span', {'color': 'error.default'}):
                        event_type = 'Cancelled'
                    else:
                        event_type = 'Not started'
                else:
                    event_type = 'Finished'
            else:
                event_type = 'Not info'


            item = {
                'name': event.find('span', {'class': 'sc-eDWCr dmsqzG'}).text,
                'type': event_type,
                'season': season,
                'category_id': category
            }

            self.parsed_data.append(item)

    def download_data(self):
        categories_to_data = []
        self.connect_to_page(self.driver, 'motorsport')
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        categories = soup.find_all('div', {'class': ['sc-hLBbgP hZQXu', 'sc-hLBbgP fdbWgV']})
        category = 1
        for cat in categories:
            url = cat.find("a")["href"]
            categories_to_data.append({'name': url.split('/')[3]})
            if self.connect_to_page(self.driver, url):
                self.driver.find_element(By.CLASS_NAME, 'dropdown-wrap').click()
                seasons = len(self.driver.find_elements(By.XPATH, "//ul[contains(@id,'downshift-0-menu')]/li"))
                self.driver.find_element(By.CLASS_NAME, 'dropdown-wrap').click()
                for season in range(0, seasons):
                    self.driver.find_element(By.CLASS_NAME, 'dropdown-wrap').click()
                    if season > 7:
                        element = self.driver.find_element(By.ID, f'downshift-0-item-{seasons - 1}')
                        self.driver.execute_script("arguments[0].scrollIntoView();", element)
                    self.driver.implicitly_wait(10)
                    season_block = self.driver.find_element(By.ID, f'downshift-0-item-{season}')
                    season_text = season_block.text
                    season_block.click()
                    time.sleep(2) # слабое место
                    page = self.driver.page_source
                    self.parse_html(page, category, season_text)
            category += 1
        self.db.record_motor_categories(categories_to_data)
        self.db.record_motorsports(self.parsed_data)

    def run(self):
        start_time = time.time()
        self.download_data()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed run time: {elapsed_time} seconds")


if __name__ == "__main__":
    webparser = WebParser()
    webparser.run()

