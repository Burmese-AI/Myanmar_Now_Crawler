from config import setup_logger
from selenium.webdriver.chrome.webdriver import WebDriver

from .worker import MyanmarNowWorker

class MyanmarNowCrawler:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = setup_logger(__name__)
        self.worker = MyanmarNowWorker()

    def crawl(self):
        self.driver.get("https://www.myanmarnow.com/")
        self.logger.info("Crawling Myanmar Now")

        # Wait for the page to load
        self.driver.implicitly_wait(10)

        # Get the page source
        page_source = self.driver.page_source
        print(page_source)

        self.worker.run()

