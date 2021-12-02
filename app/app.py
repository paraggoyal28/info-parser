from flask import Flask, render_template, request
from feedparser import FeedParser


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', feeds=[])


@app.route("/add", methods=['POST', 'GET'])
def add_url():
    if request.method == 'POST':
        try:
            print(request.form)
            feed_url = request.form['url']
            print(feed_url)
            rssParser = FeedParser(feed_url)
            rssParser.validate_input()
            feeds = rssParser.get_feeds()
            print(feeds)
            return render_template('home.html', feeds=feeds)
        except Exception as error:
            return render_template('form.html', error=error)
    else:
        return render_template('form.html', error=None)


if __name__ == "__main__":
    app.run()
