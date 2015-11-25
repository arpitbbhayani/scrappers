import os, json

from optparse import OptionParser


m_categories = {}
m_nicknames = {}

def process(file_path, process_nicks, process_categories):
    """
    Processes JSON file
    """
    file_path_abs = os.path.abspath(file_path)

    basename = os.path.basename(file_path_abs)
    directory = os.path.dirname(file_path_abs)

    with open(file_path_abs, 'rb') as infile:
        for line in infile:
            j = json.loads(line)

            page_title = j['title']
            page_links = j['links']
            page_categories = j['categories']

            if process_categories and len(page_categories) > 0:
                if not m_categories.has_key(page_title):
                    m_categories[page_title] = set()

                for category in page_categories:
                    c = category['name'].strip('| ')
                    m_categories[page_title].add(c)

            if process_nicks and len(page_links) > 0:
                for link in page_links:
                    page = link['to'].strip('| ')
                    nick = link['text'].strip('| ')
                    if not m_nicknames.has_key(page):
                        m_nicknames[page] = set()
                    m_nicknames[page].add(nick)

    with open(os.path.join(directory, 'categories', basename + '.cat'), 'wb') as cat_file:
        for key, value in m_categories.iteritems():
            json.dump({'title': key, 'categories': list(value)}, cat_file)
            cat_file.write('\n')

    with open(os.path.join(directory, 'nicknames', basename + '.nick'), 'wb') as nick_file:
        for key, value in m_nicknames.iteritems():
            json.dump({'title': key, 'nicknames': list(value)}, nick_file)
            nick_file.write('\n')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",
                  help="json file for parsing", metavar="FILE")
    parser.add_option("-n", "--nicks",
                  action="store_true", dest="nicks", default=False,
                  help="process nicks of each page")
    parser.add_option("-c", "--categories",
                  action="store_true", dest="categories", default=False,
                  help="process categories of each page")

    (opts, args) = parser.parse_args()

    if opts.file:
        process(opts.file, opts.nicks, opts.categories)
