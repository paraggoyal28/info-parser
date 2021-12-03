import validators


class Util:
    def __init__(self, url):
        self.url = url

    def checkValidUrl(self):
        """Checks for input is valid url"""

        valid = validators.url(self.url)
        if not valid:
            raise SystemExit("This url is not valid: " + self.url)
