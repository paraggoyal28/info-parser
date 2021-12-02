import requests
from bs4 import BeautifulSoup
from rssitem import RssItem


class RssReader:
    """The class handles the fetching and parsing of the rss xml from the url"""

    def __init__(self, feed_url):
        self.feed_url = feed_url

    def get_data(self):
        """Fetching the rss xml from the url"""
        try:
            response = requests.get(self.feed_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)
        return response

    def parse_data_from_rss_xml(self):
        """Parsing the rss xml and fetching all the rss items"""
        try:
            soup = BeautifulSoup(self.get_data().text, 'xml')
            return soup.findAll('item')
        except Exception as error:
            print("The xml from " + self.feed_url +
                  " cannot be parsed. Please try different url")
            raise SystemExit(error)

    def get_feeds(self):
        """Get the rss feed items"""
        items = self.parse_data_from_rss_xml()
        rss_items = []
        for item in items:
            print(item)
            rss_items.append(RssItem(item.title and item.title.text,
                                     item.description and item.description.text,
                                     item.link and item.link.text,
                                     item.pubDate and item.pubDate.text))
        return rss_items
