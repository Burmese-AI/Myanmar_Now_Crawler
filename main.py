from news_web.myanmar_now.crawler import MyanmarNowCrawler
from config import setup_chrome

def main():
    driver = setup_chrome()
    crawler = MyanmarNowCrawler(driver)
    news =crawler.crawl('https://myanmar-now.org/en/news/category/news/')
    print(news)

if __name__ == "__main__":
    main()
