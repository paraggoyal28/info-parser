from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from feedparser import FeedParser
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'supersecret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class RSSUrl(db.Model):
    __tablename__ = 'rssurl'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(4000), nullable=False)
    rssitems = relationship("RSSItem", back_populates="rssurl")

    def __init__(self, url):
        self.url = url

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class RSSItem(db.Model):
    __tablename__ = 'rssitem'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(4000), nullable=False)
    description = db.Column(db.String(40000), nullable=False)
    link = db.Column(db.String(4000), nullable=False)
    pubDate = db.Column(db.String(4000), nullable=False)
    rssurl_id = db.Column(db.Integer, db.ForeignKey('rssurl.id'))
    rssurl = relationship("RSSUrl", back_populates="rssitems")

    def __init__(self, title, description, link, pubDate):
        self.title = title
        self.description = description
        self.link = link
        self.pubDate = pubDate

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


db.create_all()
db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    feeds = []
    if 'url' in session and session['url'] is not None:
        url = RSSUrl.query.filter_by(url=session['url']).first()
        feeds = url and url.rssitems
    return render_template('home.html', feeds=feeds or [])


@app.route("/add", methods=['POST', 'GET'])
def add_url():
    if request.method == 'POST':
        try:
            feed_url = request.form['url']
            url = RSSUrl.query.filter_by(url=feed_url).first()
            if(url is not None):
                session['url'] = url.url
                return redirect(url_for('home'))
            rssParser = FeedParser(feed_url)
            rssParser.checkValidUrl()
            rss_url = RSSUrl(feed_url)
            db.session.add(rss_url)
            feeds = rssParser.fetch_feeds()
            session['url'] = feed_url
            for feed in feeds:
                rss_feed = RSSItem(
                    feed.title, feed.description, feed.link, feed.pubDate)
                rss_feed.rssurl = rss_url
                db.session.add(rss_feed)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as error:
            return render_template('form.html', error=error)
    else:
        return render_template('form.html', error=None)


@app.route("/urls", methods=['GET', 'POST'])
def fetch_urls():
    if request.method == 'POST':
        try:
            feed_url = request.form['url']
            url = RSSUrl.query.filter_by(url=feed_url).first()
            if(url is not None):
                session['url'] = url.url
                return redirect(url_for('home'))
        except Exception:
            return redirect(url_for('home'))
    else:
        urls = RSSUrl.query.all()
        return render_template('display.html', urls=urls)


if __name__ == "__main__":

    app.run()
