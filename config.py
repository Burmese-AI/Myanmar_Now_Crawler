import logging

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def setup_logger(name):
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    return logging.getLogger(name)


def setup_chrome():
    logger = setup_logger(__name__)

    user_agent = UserAgent().random
    logger.info("user agent created")

    #chrome_options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(
        #service=Service(ChromeDriverManager().install()),
        options=options
    )

    logger.info(f"Chrome driver set up with User-Agent: {user_agent}")
    return driver
