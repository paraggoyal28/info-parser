from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/feed/", methods=['POST', 'GET'])
def feed_reader():
    if request.method == 'POST':
        try:
            feed_url = request.form['url']
            feed = feedparser.parse(feed_url)
            entries = []
            entries.extend(feed.entries)

            return render_template('feed_reader.html', entries=entries)

        except:
            return "The scraping job failed. Try again."


if __name__ == "__main__":
    app.run()
