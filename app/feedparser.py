from rssfeedreader import RssReader
import validators


class FeedParser:
    def __init__(self, url):
        self.url = url
        self.rssReader = RssReader(self.url)

    def checkValidUrl(self):
        """Checks for input is valid url"""
        valid = validators.url(self.url)
        if not valid:
            raise SystemExit("This url is not valid: " + self.url)

    def fetch_feeds(self):
        "Fetches the feeds"
        return self.rssReader.fetch_feeds()
