import os

from scrapy.dupefilters import RFPDupeFilter

class URLFilter(RFPDupeFilter):
    """A dupe filter that considers specific ids in the url"""

    def __getid(self, url):
        return url

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
