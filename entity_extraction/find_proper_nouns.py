#! /usr/bin/env python
from __future__ import print_function
import io
import nltk
import yaml
from collections import defaultdict
import operator


def test_strings(contents):
    tokenizedSentence = nltk.tokenize.word_tokenize(contents)
    taggedSentence = nltk.tag.pos_tag(tokenizedSentence)
    return taggedSentence


def test_file(filename):
    with io.open(filename, 'r') as infile:
        contents = unicode(infile.read()).encode("ascii", "replace")
        return test_strings(contents)


def cleanup_output(output):
    names = []
    current = []
    for word, tag in output:
        if tag == "NNP":
            current.append(word)
        elif current:
            names.append(current)
            current = []
    return names


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--strings")
    parser.add_argument("-f", "--filename")
    parser.add_argument("-c", "--cleanup", action="store_true", default=False)
    #parser.add_argument("-m", "--model", default="3", choices=("3", "4", "7", "combi"))
    args = parser.parse_args()
    if not args.strings and not args.filename:
        raise argparse.ArgumentTypeError("Must provide either a filename or a string")

    if args.filename:
        output = test_file(args.filename)
    else:
        output = test_strings(args.strings)

    if args.cleanup:
        output = cleanup_output(output)

    print(yaml.dump(output))
