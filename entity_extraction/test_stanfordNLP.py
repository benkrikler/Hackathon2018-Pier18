#! /usr/bin/env python
from __future__ import print_function
from nltk.tag import StanfordNERTagger
import yaml
from collections import defaultdict
import operator


def build_model(model):
    if model == "3":
        return StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
    if model == "7":
        return StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz')
    if model == "4":
        return StanfordNERTagger('english.conll.4class.distsim.crf.ser.gz')
    if model == "combi":
        class Model():
            three = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
            seven = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz')
            def tag(self, contents):
                three_tags = three.tag(contents)
                seven_tags = seven.tag(contents)



def test_strings(model, contents):
    return model.tag(contents)


def test_file(model, filename):
    with open(filename, 'r') as infile:
        contents = infile.read().split()
        return test_strings(model, contents)


def cleanup_output(output):
    new_output = [(w.encode('utf-8'), e.encode('utf-8')) for w, e in output if e != 'O']
    entities = {}
    for word, entity in new_output:
        if entity not in entities:
            entities[entity] = defaultdict(int)
        entities[entity][word] += 1
    output = {}
    for entity, words in entities.items():
        output[entity] = map(list,sorted(words.items(), key=operator.itemgetter(1), reverse=True))

    return output


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--strings")
    parser.add_argument("-f", "--filename")
    parser.add_argument("-c", "--cleanup", action="store_true", default=False)
    parser.add_argument("-m", "--model", default="3", choices=("3", "4", "7", "combi"))
    args = parser.parse_args()
    if not args.strings and not args.filename:
        raise argparse.ArgumentTypeError("Must provide either a filename or a string")

    model = build_model(args.model)
    if args.filename:
        output = test_file(model, args.filename)
    else:
        output = test_strings(model, args.strings.split())

    if args.cleanup:
        output = cleanup_output(output)

    print(yaml.dump(output))
