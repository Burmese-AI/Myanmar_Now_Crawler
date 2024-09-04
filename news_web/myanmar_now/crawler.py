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

    def crawl_data_from_home(self, container_selector : str, a_tag : str) -> Optional[list[str]]:
        links = self.worker.get_news_links_from_home_page(container_selector, a_tag)

        if not links:
            self.logger.warning('there is no links')
            return None

        return links



    def crawl_data_from_article(self, url : str) -> Optional[Article]:
        return self.worker.format_news(url)


    def crawl(self, url : str) -> Union[
        Optional[Article],
        Optional[list[Article]],
        Optional[list[str]]
    ]:

        #for english language
        home_url = 'https://myanmar-now.org'
        category_url = 'https://myanmar-now.org/en/news/category'
        article_url = 'https://myanmar-now.org/en/news'

        #for myanmar language
        mm_home_url = 'https://myanmar-now.org/mm'
        mm_category_url = 'https://myanmar-now.org/mm/news/category'
        mm_article_url = 'https://myanmar-now.org/mm/news'

        self.driver.get(url)

        if "Page not found" in self.driver.title:
            self.logger.warning(f'{url} is not existed in Myanmar Now')
            return None

        self.logger.info("started crawling Myanmar Now")

        #what if url is category url
        if category_url in url:
            self.logger.info("crawling category url")

            return self.crawl_data_from_page(
                '[role="main"]',
                'a.more-link.button')

        #what if url is mm category url
        elif mm_category_url in url:
            self.logger.info("crawling mm category url")

            return self.crawl_data_from_page(
                '[role="main"]',
                'a.more-link.button')

        #what if url is article url
        elif article_url in url:
            self.logger.info("crawling article url")

            return self.crawl_data_from_article(url)

        #what if url is mm article url
        elif mm_article_url in url:
            self.logger.info("crawling mm article url")

            return self.crawl_data_from_article(url)

        #what if url is mm home url
        elif mm_home_url in url:
            self.logger.info("crawling mm home url")

            return self.crawl_data_from_page(
                '#tiepost-37659-section-1135',
                'div.slide.tie-standard.slick-slide.slick-cloned h2 a')

        #what if url is home url
        elif home_url in url:
            self.logger.info("crawling home url")

            return self.crawl_data_from_home(
                'div.main-content.tie-col-md-12',  #tiepost-21224-section-3016
                'div.slide.tie-standard.slick-slide.slick-cloned h2 a')

        else:
            self.logger.warning(f'{url} is not existed in Myanmar Now')
            return None


