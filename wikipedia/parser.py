import xml.etree.ElementTree as ET

namespaces = {
    'page': 'http://www.mediawiki.org/xml/export-0.10/'
}


tree = ET.parse('/Users/arpitbhayani/Downloads/enwiki-latest-pages-articles1.xml-p000000010p000010000')

page = tree.find('page:page[0]', namespaces)
