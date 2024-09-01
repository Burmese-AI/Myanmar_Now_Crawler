from news_web.myanmar_now.crawler import MyanmarNowCrawler
from config import setup_chrome

def main():
    driver = setup_chrome()
    crawler = MyanmarNowCrawler(driver)
    news =crawler.crawl('url you want to crawl in Myanmar Now website')
    print(news)

if __name__ == "__main__":
    main()
