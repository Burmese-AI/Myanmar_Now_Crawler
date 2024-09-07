from typing import Optional

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from config import setup_logger
from model.article import Article


class MyanmarNowWorker:
    def __init__(self, driver: WebDriver):
        self.logger = setup_logger(__name__)
        self.driver = driver

    def find_by_css_selector(self, input : str) -> Optional[WebElement] :
        try:
            return self.driver.find_element(By.CSS_SELECTOR, input)
        except Exception as e:
            self.logger.error(f'Error - {e}')
            return None


    def extract_text(self, element : Optional[WebElement]) -> Optional[str] :
        if element:
            return element.text
        else :
            self.logger.error(f'{element} not found')
            return None


    def get_news_links(self, container_selector: str, a_tag: str) -> Optional[list[str]] :
        try:
            links = []

            container = self.find_by_css_selector(container_selector)

            a_tags = container.find_elements(By.CSS_SELECTOR, a_tag)

            for a in a_tags:
                links.append(a.get_attribute('href'))

            self.logger.info(f'Gathered {len(links)} links')
            return links

        except Exception as e:
            self.logger.error(f'Error - {e}')
            return None


    def get_category_links(self)  :
        try:
            links = []
            container = self.find_by_css_selector('div#main-nav-menu.main-menu.header-menu')

            list = container.find_elements(By.CSS_SELECTOR, 'li.menu-item:not(.menu-item-has-children):not(.menu-item-has-icon)')

            for li in list:
                links.append(li.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

            self.logger.info(f'Gathered {len(links)} links from nav bar')
            return links

        except Exception as e:
            self.logger.error(f'Error - {e}')
            return None

    def get_news_links_from_home_page(self, container_selector: str, a_tag: str) -> Optional[list[str]] :
        try:
            links = []

            containers = self.driver.find_elements(By.CSS_SELECTOR, container_selector)

            for container in containers:
                a_tags = container.find_elements(By.CSS_SELECTOR, a_tag)

                for a in a_tags:
                    links.append(a.get_attribute('href'))

            self.logger.info(f'Gathered {len(links)} links')
            return links

        except Exception as e:
            self.logger.error(f'Error - {e}')
            return None


    def format_news(self, link : str) -> Optional[Article] :
            self.driver.get(link)
            try:
                title = self.find_by_css_selector('h1.post-title.entry-title')
                title = self.extract_text(title)

                sub_title =  self.find_by_css_selector('h2.entry-sub-title')
                sub_title = self.extract_text(sub_title)

                date = self.find_by_css_selector('span.date.meta-item.tie-icon')
                date = self.extract_text(date)

                entry_content = self.find_by_css_selector('div.entry-content.entry.clearfix')
                content = "\n" .join([p.text for p in entry_content.find_elements(By.XPATH, './p')])

                self.logger.info(f'\n{title} \n{date}')
                return Article(
                    title=title,
                    subtitle=sub_title,
                    date=date,
                    content=content,
                    source=link
                )

            except Exception as e:
                self.logger.error(f'format news error - {e}')
                return None
