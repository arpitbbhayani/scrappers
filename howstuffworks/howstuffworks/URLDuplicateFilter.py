import os

from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint

import logging
logger = logging.getLogger(__name__)

class URLFilter(RFPDupeFilter):
    """A dupe filter that considers specific ids in the url"""

    def __getid(self, url):
        mm = url
        return mm

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
