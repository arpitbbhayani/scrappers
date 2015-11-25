import os, json
import re, requests
import xml.etree.ElementTree as ET

from optparse import OptionParser
from BeautifulSoup import BeautifulSoup

namespaces = {
    'page': 'http://www.mediawiki.org/xml/export-0.10/'
}

links_filter = re.compile('\[\[[a-zA-Z0-9_ ]*:')


def process_links(raw_links):
    links = []
    for raw_link in raw_links:
        link = raw_link[2:-2]
        index = link.find('|')
        if index != -1:
            to = link[:index]
            text = link[index:]
        else:
            to = link
            text = link

        index = to.find('#')
        if index != -1:
            to = to[:index]

        to = to.strip().lower()
        text = text.strip().lower()

        if len(text) == 0:
            text = to

        links.append({
            'to'   : to,
            'text' : text
        })
    return links


def process_categories(raw_categories):
    categories = []
    for raw_category in raw_categories:
        category = raw_category[11:-2].strip().lower()
        categories.append({
            'name': category
        })
    return categories


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
            pass
        else:
            raw_links.append(entity)
        start_index = page_content.find('[[', end_index+2)

    links = process_links(raw_links)
    categories = process_categories(raw_categories)
    return links, categories


def process(file_path):
    dis_file = file_path + '.dis'
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

        links, categories = process_wiki(page_content)

        data = {
            'id': page_id.strip(),
            'title': page_title.strip().lower(),
            'links': links,
            'categories': categories
        }

        possible_dis = False
        for category in categories:
            if "disambiguation" in category['name']:
                possible_dis = True

        if 'disambiguation' in page_title.lower():
            possible_dis = True

        if possible_dis:
            with open(dis_file, 'a') as outfile:
                json.dump(data, outfile)
                outfile.write('\n')
        else:
            with open(json_file, 'a') as outfile:
                json.dump(data, outfile)
                outfile.write('\n')
                print 'id:', page_id


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",
                  help="file for parsing", metavar="FILE")

    (opts, args) = parser.parse_args()

    if opts.file:
        process(opts.file)
