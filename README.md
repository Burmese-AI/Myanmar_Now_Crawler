# News Crawler

This project is a simple news crawler that uses Selenium to crawl news from the **[Myanmar Now](https://myanmar-now.org/en/)**. 

web app and telegram bot are here:
- [News crawler web](https://newscrawler-1.onrender.com/)
- [@nyu_spider_bot](https://t.me/nyu_spider_bot) (you need to run tele bot file)

**[Note: Please read the concerns first](#concerns)**


## Features

- Request URLs from users with depth options [1, 2, 3].
- Crawl data from URLs with specified depth options.
- Send crawled data (may include multiple links or articles) back to users.
- Enable downloading of a single article in HTML format.


## Installation

clone this repo

```bash
git clone https://github.com/zwemarnhtay/NewsCrawler.git
```

install dependencies

```bash
pip install -r requirements.txt
```


## Run Locally

- To run crawler web app
```bash
python app.py
```

- To run telegram bot
```bash
python -m tele_bot.bot
```

## Concerns

### Loading Time
Using this Telegram bot or [this deployed web application](https://newscrawler-1.onrender.com/) may result in long loading times.

### Potential Out of Memory Error
Crawling data with depth options [2, 3] in the Telegram bot or [this deployed web application](https://newscrawler-1.onrender.com/) may lead to server errors due to memory limitations.
