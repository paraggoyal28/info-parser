from rssfeedreader import RssReader


class FeedParser:
    def __init__(self, url):
        self.url = url
        self.rssReader = RssReader(self.url)

    def fetch_feeds(self):
        "Fetches the feeds"
        return self.rssReader.fetch_feeds()
