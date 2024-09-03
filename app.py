from flask import Flask, request, render_template, jsonify

from news_web.myanmar_now.crawler import MyanmarNowCrawler
from config import setup_chrome


driver = setup_chrome()
mn_crawler = MyanmarNowCrawler(driver)


app = Flask(__name__, template_folder='./UI')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crawl', methods=['POST'])
def crawl():
    try:
        data = request.form
        url = data.get('url')

        print(f"requested URL: {url}")
        news = mn_crawler.crawl(url)
        print(news)

        if not isinstance(news, list):
            news = [news]

        response = [article.__dict__ for article in news]

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
