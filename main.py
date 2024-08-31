from news_web.myanmar_now.crawler import MyanmarNowCrawler
from config import setup_chrome

def main():
    driver = setup_chrome()
    crawler = MyanmarNowCrawler(driver)
    crawler.crawl()

if __name__ == "__main__":
    main()
