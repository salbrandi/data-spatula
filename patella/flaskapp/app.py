from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/patella/<url>')
def flask_scrape(url):
    return render_template('page.html', url=url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
