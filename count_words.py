#!/usr/bin/env python3

"""Print the most frequent words found on stdin to stdout with their count.

Words are combined if they have a common root and the most frequently occurring
variant is used.

The sqrt of the frequency of the word is used.

e.g.

./count_words.py --grouping=stem <<EOF
run
running
running
running
runs
runs
fox
foxes
EOF
6	running
2	fox
"""

import argparse
import collections
import math
import sys

from nltk.stem import snowball



def flatten_dict_of_counts(count_of_counts):
    flat_count = collections.Counter()
    for item, counts in count_of_counts.items():
        word, _ = counts.most_common(1).pop()
        flat_count[word] = sum(counts.values())
    return flat_count


def stemmed_count(words):
    stemmed_to_variant_counter = collections.defaultdict(collections.Counter)
    stemmer = snowball.EnglishStemmer()

    for word in words:
        normalized_word = stemmer.stem(word).lower()
        stemmed_to_variant_counter[normalized_word][word] += 1

    return flatten_dict_of_counts(stemmed_to_variant_counter)


def case_normalized_count(words: [str]):
    case_to_variant_counter = collections.defaultdict(collections.Counter)
    for word in words:
        case_to_variant_counter[word.lower()][word] += 1
    return flatten_dict_of_counts(case_to_variant_counter)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-words",
        dest='num_words',
        default=100,
        type=int,
        help="Print at most this many unique words.")
    parser.add_argument(
        '--grouping',
        default='none',
        choices=['none','case','stem'],
        help='The method to use when deciding if words are the same.')
    parser.add_argument(
        '--counting',
        default='sum',
        choices=['sum', 'sqrt', 'log'],
        help='The method used to calculate the weight of each word.')

    args = parser.parse_args()

    words = (word.strip() for word in sys.stdin.readlines())
    if args.grouping == 'case':
        counts = case_normalized_count(words)
    elif args.grouping == 'stem':
        counts = stemmed_count(words)
    else:
        counts = collections.Counter(words)

    summer = {
        'sum': lambda x: x,
        'sqrt': math.sqrt,
        'log': math.log10,
    }[args.counting]
    for word, frequency in counts.most_common(args.num_words):
        biased = summer(frequency)

        print(round(biased), word, sep='\t')


if __name__ == '__main__':
    main()
