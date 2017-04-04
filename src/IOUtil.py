#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import logging
import re
import Toptopics

url_pattern = 'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
url_regex = re.compile(url_pattern)
not_ascii_pattern = '[^\x00-\x7F]+'
not_ascii_regex = re.compile(not_ascii_pattern)
rebundant_characters = re.compile('@[a-zA-Z0-9_:]+|#|&lt|RT')

logging.basicConfig(
        level=logging.INFO,
        format=('[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d :'
                '%(message)s'), datefmt='%a, %d %b %Y %H:%M:%S')


def decode_string(input_str):
    # type: (str) -> str
    try:
        return str.strip(input_str).decode('utf8')
    except ValueError as err:
        logging.warning('Failed to decode string {0}'.format(err))
        return ''


def read_file(file_path, process=None):
    contents_list = list()
    try:
        with open(file_path) as input_file:
            for line in input_file:
                new_line = not_ascii_regex.sub('', line)
                new_line = decode_string(new_line)
                if process:
                    new_line = process(new_line)
                if new_line:
                    contents_list.append(new_line)

            return contents_list

    except IOError as err:
        logging.warning('Failed to open file {0}'.format(err.message))
        sys.exit(1)


def fold_left(regex_list):
    def process_string(input_string):
        for regex in regex_list:
            input_string = regex.sub('', input_string)
        input_string = input_string.strip()
        return input_string

    return process_string

if __name__ == '__main__':
    file_path = '/Users/zxj/Downloads/algorithm_project/data_7_gen_2_plain.txt'
    regex_list = [url_regex, rebundant_characters]
    contents = read_file(file_path, process=fold_left(regex_list))
    key_words = Toptopics.key_words(contents)
    for ele in key_words:
        print ele