from rssfeedreader import RssReader
import validators


class FeedParser:
    def __init__(self, url):
        self.url = url

    def validate_input(self):
        """Checks for input is valid url"""
        valid = validators.url(self.url)
        if not valid:
            raise SystemExit("This url is not valid: " + self.url)

    def get_feeds(self):
        "Get the feed from the url"
        return RssReader(self.url).get_feeds()
