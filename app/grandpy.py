#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module used for GrandPy Bot
Stopword list used from https://github.com/stopwords-iso/stopwords-fr/blob/master/stopwords-fr.json
"""
import json, os, string, requests


class BotResponse:

    def __init__(self, user_message):
        self.user_message = user_message
        self.user_message_parsed = self.parse_text(self.user_message)
        self.wiki_repsonse = ""
        self.googlemaps_response = ""
        self.lng = 0
        self.lat = 0

    def parse_text(self, user_message):
        """Parses the given input_tex. Sets chars to lowerkey, strips punctuation and removes words that are in stopwords.json

        :param user_message: The text to parse
        :type user_message: string

        :rtype: string
        """
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/stopwords.json') as f:
                stopwords = json.load(f)
        except IOError as err:
            print('Error loading stopword file : ' + str(err))
            stopwords = "error"
        # Remove all punctuation and make text lowercase
        translator = str.maketrans('', '', string.punctuation)
        parsed_text = user_message.lower().translate(translator)
        for word in parsed_text.split():
            if word in stopwords:
                parsed_text = parsed_text.replace(word, "",1)
            parsed_text = " ".join(parsed_text.split())
        return parsed_text


def get_wiki_info(input_text):

    api_lnk = 'https://fr.wikipedia.org/w/api.php'
    api_parm = '?action=query&prop=extracts&exintro&explaintext&format=json&exsentences=5&titles='+input_text
    json_wiki = json.loads(requests.get(api_lnk+api_parm).text)
    article_id = list(json_wiki['query']['pages'].keys())[0]
    try:
        wiki_article_intro = json_wiki['query']['pages'][article_id]['extract']
    except KeyError:
        wiki_article_intro = "No result"
    return wiki_article_intro

