import os, json
import re, requests
import xml.etree.ElementTree as ET

from optparse import OptionParser
from BeautifulSoup import BeautifulSoup

namespaces = {
    'page': 'http://www.mediawiki.org/xml/export-0.10/'
}

links_filter = re.compile('\[\[[a-zA-Z0-9_]+:')

def get_links(html_content):
    links = []
    soup = BeautifulSoup(html_content)
    for link in soup.findAll('a', attrs={'href': re.compile("^/wiki/")}):
        href = link.get('href')
        anchor_text = link.getText().strip()
        if len(anchor_text) > 0 and not links_filter.match(href):
            links.append({
                'href': href,
                'text': anchor_text
            })
    return links


def process_wiki(page_content):
    raw_links, raw_categories = [], []

    start_index = page_content.find('[[', 0)
    while start_index != -1:
        end_index = page_content.find(']]', start_index+2)

        if end_index == -1:
            print "No end_index found for start_index %d and end_index %d" % (start_index, end_index)
            break

        entity = page_content[start_index:end_index+2]

        if entity.startswith('[[Category:'):
            raw_categories.append(entity)
        elif links_filter.match(entity):
            # Drop
            pass
        else:
            raw_links.append(entity)

        start_index = page_content.find('[[', end_index+2)

    return raw_links, raw_categories


def process(file_path):
    json_file = file_path + '.json'

    tree = ET.parse(file_path)
    pages = tree.findall('page:page', namespaces)

    for page in pages:
        page_id = page.find('page:id', namespaces).text
        page_ns = page.find('page:ns', namespaces).text
        page_title = page.find('page:title', namespaces).text
        page_content = page.find('page:revision/page:text', namespaces).text

        if page_ns != '0':
            continue

        raw_links, raw_categories = process_wiki(page_content)
        print raw_links, raw_categories


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",
                  help="file for parsing", metavar="FILE")

    (opts, args) = parser.parse_args()

    if opts.file:
        process(opts.file)
