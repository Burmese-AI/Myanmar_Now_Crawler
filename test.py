from news_web.myanmar_now.crawler import MyanmarNowCrawler
from config import setup_chrome

def testing():
    driver = setup_chrome()
    crawler = MyanmarNowCrawler(driver)
    news =crawler.crawl('https://myanmar-now.org/en', 3)
    print(news)

if __name__ == "__main__":
    testing()
