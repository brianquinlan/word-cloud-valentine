#!/usr/bin/env python3

"""Print the interesting words found on stdin to stdout.

Interesting words are defined as nouns that are not in a list of boring words.

e.g.

./extract_words.py
The rain on the plane falls mainly in Spain.
Verbs are nice too but there are too many helper verbs in English.
^D
rain
plane
Spain
Verbs
verbs
English
"""

import argparse
import re
import sys

import nltk


BLACKLIST_WORDS = [
    '%',
    "'ll",
    "'m",
    "'s",
    'are',
    'be',
    'bit',
    'could',
    'do',
    'he',
    'https',
    'i',
    'is',
    'it',
    "n't",
    'not',
    't',
    'was',
    '’']


def extract_all_words(text):
    return nltk.word_tokenize(text)


def extract_non_black_list_words(text):
    return (word for word in nltk.word_tokenize(text)
            if word.lower() not in BLACKLIST_WORDS)


def extract_tagged_words(text: str, tag_pattern: str):
    """Extract the words from the given text that match a given part-of-speech.

    Args:
        text: A piece of English text. Ideally grammatical.
        tag_pattern: A regular expression that matches the nntk tags of words
            that should be returned by this function e.g. 'MD|UH' would match
            modal auxiliary verbs and interjections. Use
            nltk.help.upenn_tagset('.*') to see a complete list of tags.

    Returns:
        A list of words that whose nltk matches the given tag pattern.
    """
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    interesting_words = [word for word, tag in tagged
                         if re.match(tag_pattern, tag) and
                         word.lower() not in BLACKLIST_WORDS]
    return interesting_words


def extract_nouns(text):
    return extract_tagged_words(text, r'NN.*')


def extract_non_boring(text):
    return extract_tagged_words(text, r'(FW)|(JJ.*)|(NN.*)|(RB.*)|(UH)|(WB.*)')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--interesting-words',
        dest='interesting_words',
        default='all',
        choices=['all', 'non-blacklist', 'non-boring', 'nouns'],
        help='The method to use when deciding if words are the same.')
    args = parser.parse_args()

    extractor = {
        'all': extract_all_words,
        'non-blacklist': extract_non_black_list_words,
        'non-boring': extract_non_boring,
        'nouns': extract_nouns}[args.interesting_words]

    for text in sys.stdin.readlines():
        text = text.strip()
        for word in extractor(text):
            print(word)


if __name__ == '__main__':
    main()
