#! /usr/bin/env python
from __future__ import print_function
import io
import spacy
import yaml
from collections import defaultdict
import operator
import re


_whitespace_re = re.compile(r"\s+")


def test_strings(contents):
    nlp = spacy.load('en')
    return nlp(contents)

def test_file(filename):
    with io.open(filename, 'r') as infile:
        contents = unicode(infile.read()) #.replace("\n", "")
        return test_strings(contents)

def clean_string(string):
    return _whitespace_re.sub(" ", string.encode('utf-8')).strip()

def cleanup_output(output):
    output = [(out.text, out.label_) for out in output.ents]

    new_output = [(clean_string(w), e.encode('utf-8')) for w, e in output if w != '\n']
    entities = {}
    for word, entity in new_output:
        if entity not in entities:
            entities[entity] = defaultdict(int)
        entities[entity][word] += 1
    output = {}
    for entity, words in entities.items():
        output[entity] = map(list,sorted(words.items(), key=operator.itemgetter(1), reverse=True))
    return output

def plot_results(entities):
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    n_entities = len(entities)
    labels = []
    data = []
    for x, (entity, words) in enumerate(entities.items()):
        labels.append(entity)
        y = 0
        for word, score in words:
            if score < 2:
                continue
            try:
                data.append((x, y, score, word.encode("utf-8","replace")))
            except UnicodeDecodeError:
                print("BEK", word)
                continue
            y += score*2

    data = pd.DataFrame(data, columns="x y score label".split())
    ax = plt.subplot(111)
#    data.x += np.random.normal(0, 1, len(data))
    ax.scatter(data.x, data.y, s=data.score**2*6, c=data.score)
    map(lambda data: ax.text(*data, size=9, horizontalalignment='center',rotation=45),zip(data.x, data.y, data.label))
    ax.set_xticklabels(labels)
    plt.xticks(range(n_entities))
    plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--strings")
    parser.add_argument("-f", "--filename")
    parser.add_argument("-p", "--plot", action="store_true", default=False)
    parser.add_argument("-c", "--cleanup", action="store_true", default=False)
    #parser.add_argument("-m", "--model", default="3", choices=("3", "4", "7", "combi"))
    args = parser.parse_args()
    if not args.strings and not args.filename:
        raise argparse.ArgumentTypeError("Must provide either a filename or a string")

    if args.filename:
        output = test_file(args.filename)
    else:
        output = test_strings(args.strings.split())

    if args.cleanup or args.plot:
        output = cleanup_output(output)

    if args.plot:
        plot_results(output)

    print(yaml.dump(output))
    #print(output)
