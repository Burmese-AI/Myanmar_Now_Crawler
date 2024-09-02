from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder='./UI')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crawl', methods=['POST'])
def crawl():
    print(f"Received request: {request.form}")
    try:
        data = request.form
        url = data.get('url')
        print(f"Crawling URL: {url}")
        return jsonify({'message': 'Crawling started', 'url': url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
