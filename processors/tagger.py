import os
import json
from optparse import OptionParser

import nltk

def parse(file_path):
    """
    Given a file 'file_path', returns list of tags
    """
    with open(file_path, 'rb') as f:
        contents = json.loads(f.read())
        print extract_tags(contents['desc'])


#
# https://en.wikipedia.org/w/api.php?action=query&clshow=!hidden&cllimit=500&prop=categories&titles=Sachin_Tendulkar
#

def extract_tags(content):
    """
    Given string content, returns list of tags
    """
    tag, tags = [], []
    pos_tags = ['NN', 'NNP', 'NNS', 'NNPS']
    for pos_element in nltk.pos_tag(content.split()):
        if pos_element[1] in pos_tags:
            tag.append(pos_element)
        else:
            if len(tag) > 0:
                tags.append(tag)
            tag = []
    if len(tag) > 0:
        tags.append(tag)

    return tags

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="directory",
                  help="all files of this directory will be parsed", metavar="DIR")
    parser.add_option("-f", "--file", dest="file",
                  help="file for parsing", metavar="FILE")

    (opts, args) = parser.parse_args()

    if opts.file:
        parse(opts.file)

    if opts.directory:
        files = os.listdir(opts.directory)
        for file_name in files:
            file_path = os.path.join(opts.directory, file_name)
            parse(file_path)
