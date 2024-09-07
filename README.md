# News Crawler

This project is a simple news crawler that uses Selenium to crawl news from the **[Myanmar Now](https://myanmar-now.org/en/)**. Unfortunately, this web app is need to be deployed for production.

## Features

- request urls from users with depth options [1, 2, 3]
- crawl data from url with depth options
- send crawled data [may be multiple links or articles] back to user
- enable to download single article with html format


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

```bash
python app.py
```

## Todo

- [ ] Deploy this app
- [ ] Integrate with Telegram Bot

