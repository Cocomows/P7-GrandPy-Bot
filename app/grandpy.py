#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module used for GrandPy Bot
Stopword list used from https://github.com/stopwords-iso/stopwords-fr/blob/master/stopwords-fr.json
"""
import json, os, string


def parseText(input_text):
    try:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/stopwords.json') as f:
            stopwords = json.load(f)
    except IOError as err:
        print('Error loading stopword file : ' + str(err))
        stopwords = "error"
    # Remove all punctuation and make text lowercase
    translator = str.maketrans('', '', string.punctuation)
    parsed_text = input_text.lower().translate(translator)
    for word in parsed_text.split():
        if word in stopwords:
            parsed_text = parsed_text.replace(word+" ", "")
        parsed_text = " ".join(parsed_text.split())
    return parsed_text


