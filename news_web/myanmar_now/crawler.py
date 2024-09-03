from typing import Optional, Union

from config import setup_logger
from model.article import Article
from selenium.webdriver.chrome.webdriver import WebDriver

from .worker import MyanmarNowWorker


class MyanmarNowCrawler:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = setup_logger(__name__)
        self.worker = MyanmarNowWorker(driver)


    #to crawl data from page containing multiple articles
    def crawl_data_from_page(self,
                             container : str,
                             a_tag : str) -> Optional[list[Article]]:

        news_list : list[Article] = []

        #get all news links from page
        links = self.worker.get_news_links(container, a_tag)

        if not links:
            self.logger.warning('there is no links')
            return None

        #crawl news from news links
        for link in links:
            news_list.append(self.crawl_data_from_article(link))

        return news_list


    def crawl_data_from_article(self, url : str) -> Optional[Article]:
        return self.worker.format_news(url)


    def crawl(self, url : str) -> Union[Optional[Article], Optional[list[Article]]]:
        home_url = 'https://myanmar-now.org'
        category_url = 'https://myanmar-now.org/en/news/category/'
        article_url = 'https://myanmar-now.org/en/news/'

        self.driver.get(url)

        if "Page not found" in self.driver.title:
            self.logger.warning(f'{url} is not existed in Myanmar Now')
            return None

        self.logger.info("started crawling Myanmar Now")

        #what if url is category url
        if category_url in url:
            return self.crawl_data_from_category(
                '[role="main"]',
                'a.more-link.button')

        #what if url is article url
        elif article_url in url:
            return self.crawl_data_from_article(url)

        #what if url is home url
        elif home_url in url:
            return self.crawl_data_from_page(
                '#tiepost-21224-section-3016',
                'div.slide.tie-standard.slick-slide.slick-cloned h2 a')

        else:
            self.logger.warning(f'{url} is not existed in Myanmar Now')
            return None


