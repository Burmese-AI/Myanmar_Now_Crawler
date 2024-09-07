from config import setup_chrome
from news_web.myanmar_now.crawler import MyanmarNowCrawler


def testing():
    driver = setup_chrome()
    crawler = MyanmarNowCrawler(driver)
    news = crawler.crawl("https://myanmar-now.org/en", 2)
    print(type(news[0][0]))


if __name__ == "__main__":
    testing()
