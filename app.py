from flask import (
    Flask,
    request,
    render_template,
    jsonify
)
import html

from news_web.myanmar_now.crawler import MyanmarNowCrawler
from config import setup_chrome, setup_logger
from model.article import Article


logger = setup_logger(__name__)

driver = setup_chrome()
mn_crawler = MyanmarNowCrawler(driver)


app = Flask(__name__, template_folder='./UI')
logger.info("Flask app created")

@app.route('/')
def index():
    logger.info("Index route called")
    return render_template('index.html')



@app.route('/crawl', methods=['POST'])
def crawl():
    logger.info("Crawl route called")
    try:
        data = request.form
        url = data.get('url')

        logger.info(f"requested URL: {url}")
        data = mn_crawler.crawl(url)
        logger.info(type(data))

        response = {}

        if not data:
            logger.info("No data found")
            response['error'] = 'No data found'

        if type(data) is Article :
            logger.info("data is Article")
            data = [data]
            response['articles'] = [article.__dict__ for article in data]

        elif type(data) is list and type(data[0]) is Article:
            logger.info("data is list of Article")
            response['articles'] = [article.__dict__ for article in data]

        elif type(data) is list and type(data[0]) is str:
            logger.info("data is list of links")
            #change links array to dictionary
            response['links'] = {f"link_{i}": link for i, link in enumerate(data)}

        logger.info(response)
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in crawl route: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['POST'])
def download():
    logger.info("Download route called")
    try:
        logger.info("Received data:", request.json)
        article = request.json.get('article')

        if not article:
            return "Article not found", 404

        print(article.get('title'))

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(article['title'])}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .article-card {{ background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; }}
        .article-title {{ font-size: 1.25rem; font-weight: 700; color: #1f2937; }}
        .article-subtitle {{ font-size: 1.125rem; color: #4b5563; margin-top: 0.25rem; }}
        .article-date {{ font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem; }}
        .article-content {{ margin-top: 0.75rem; }}
        .article-source {{ font-size: 0.875rem; color: #2563eb; margin-top: 0.5rem; }}
    </style>
</head>
<body>
    <div class="article-card">
        <h2 class="article-title">{html.escape(article['title'])}</h2>
        <h3 class="article-subtitle">{html.escape(article['subtitle'])}</h3>
        <p class="article-date">{html.escape(article['date'])}</p>
        <p class="article-content">{html.escape(article['content'])}</p>
        <p class="article-source">Source: {html.escape(article['source'])}</p>
    </div>
</body>
</html>
"""

        response_data = {
            "html_content": html_content,
            "filename": f"{article['title'].replace(' ', '_')}.html"
        }
        return jsonify(response_data), 200

    except Exception as e:
        logger.error("Error in download route:", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
