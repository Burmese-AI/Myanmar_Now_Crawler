from flask import (
    Flask,
    request,
    render_template,
    jsonify
)
import html

from news_web.myanmar_now.crawler import MyanmarNowCrawler
from config import setup_chrome
from model.article import Article



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
        print(type(news))

        response = {}

        if type(news) is Article :
            news = [news]
            response['articles'] = [article.__dict__ for article in news]

        elif type(news) is list and type(news[0]) is Article:
            response['articles'] = [article.__dict__ for article in news]
        else:
            #change links array to dictionary
            response['links'] = {f"link_{i}": link for i, link in enumerate(news)}

        print(response)
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['POST'])
def download():
    try:
        print("Received data:", request.json)
        article = request.json.get('article')
        print("Received data:", article)

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
        print("Error in download route:", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
