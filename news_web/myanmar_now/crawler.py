import time
from typing import Optional, Union

from selenium.webdriver.chrome.webdriver import WebDriver

from config import setup_logger
from model.article import Article

from .worker import MyanmarNowWorker


class MyanmarNowCrawler:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = setup_logger(__name__)
        self.worker = MyanmarNowWorker(driver)


    #to crawl data from page containing multiple articles
    def crawl_data_from_page(self,
              dept: int,
              container : str,
              a_tag : str
              ) -> Union[
                  Optional[list[Article]],
                  Optional[list[str]]
                  ]:

        #get all news links from page
        links = self.worker.get_news_links(container, a_tag)

        if not links:
            self.logger.warning('there is no links')
            return []

        if dept > 1 :
            dept -= 1

            news_list : list[Article] = []

            #crawl news from news links
            for link in links:
                time.sleep(1)
                news_list.append(self.crawl_data_from_article(link))

            return news_list

        #if dept option is not greater than 1, then return links
        return links


    #to crawl data from home page
    def crawl_data_from_home(self, dept : int) ->  Union[
        Optional[
            list[list[Article]]
            ],
        Optional[
            list[list[str]]
            ]
        ]:

        try:
            links = self.worker.get_category_links()

            if not links:
                self.logger.warning('there is no links')
                return None

            #if dept option is greater than 1, then crawl data from each category
            if dept > 1 :
                dept -= 1

                data_list = []

                for link in links:
                    time.sleep(2)

                    self.logger.info(f'opening {link}')
                    self.driver.get(link)

                    data = self.crawl_data_from_page(
                        dept=dept,
                        container='[role="main"]',
                        a_tag='a.more-link.button')

                    data_list.append(data)
                    self.logger.info(f'reached {link}')

                return data_list

            #if dept option is not greater than 1, then return category links
            return links

        except Exception as e:
            self.logger.error(f'Error - {e}')
            return None


    #to crawl data from article
    def crawl_data_from_article(self, url : str) -> Optional[Article]:
        return self.worker.format_news(url)


    #main crawler using from outside
    def crawl(self, url : str, dept : int = 1) -> Union[
        Optional[Article],
        Optional[list[Article]],
        Optional[list[str]],
        Optional[list[list[Article]]],
        Optional[list[list[str]]]
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
                dept=dept,
                container='[role="main"]',
                a_tag='a.more-link.button')

        #what if url is mm category url
        elif mm_category_url in url:
            self.logger.info("crawling mm category url")

            return self.crawl_data_from_page(
                dept=dept,
                container='[role="main"]',
                a_tag='a.more-link.button')

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

            return self.crawl_data_from_home(dept)

        #what if url is home url
        elif home_url in url:
            self.logger.info("crawling home url")

            return self.crawl_data_from_home(dept)

        else:
            self.logger.warning(f'{url} is not existed in Myanmar Now')
            return None


