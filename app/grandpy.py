#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module used for GrandPy Bot
Stopword list used from https://github.com/stopwords-iso/stopwords-fr/blob/master/stopwords-fr.json
"""
import json
import os
import string
import requests


class BotResponse:

    def __init__(self, user_message):
        self.user_message = user_message
        self.user_message_parsed = self.parse_text()
        if self.user_message_parsed != "" :
            self.wiki_response = self.get_wiki_info()
            self.gmaps_response = self.get_gmaps_info()
        else:
            self.wiki_response = "No result"
            self.gmaps_response = "No result"
            self.lat = 0
            self.lng = 0


    def parse_text(self):
        """Parses the attribute self.user_message. Sets chars to lowerkey, strips punctuation and removes words that are in stopwords.json

        :rtype: string
        """
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/stopwords.json') as f:
                stopwords = json.load(f)
        except IOError as err:
            print('Error loading stopword file : ' + str(err))
            stopwords = "error"
        # # Remove all punctuation and make text lowercase
        translator = str.maketrans('', '', string.punctuation)
        parsed_text = self.user_message.lower().translate(translator)

        for word in parsed_text.split():
            if word in stopwords:
                parsed_text = parsed_text.replace(word, "",1)
            parsed_text = " ".join(parsed_text.split())
        return parsed_text

    def get_wiki_info(self):
        """Gets the 5 first sentences from wikipedia for the article about the parsed text

        :rtype: string
        """
        
        api_lnk = 'https://fr.wikipedia.org/w/api.php'
        api_parm = '?action=query&prop=extracts&exintro&explaintext&format=json&indexpageids&exsentences=5&generator=search&gsrlimit=1&gsrsearch='
        api_search = self.user_message_parsed
        json_wiki = json.loads(requests.get(api_lnk + api_parm + api_search).text)
        try:
            article_id = json_wiki['query']['pageids'][0]
            wiki_article_intro = json_wiki['query']['pages'][article_id]['extract']
            title = json_wiki['query']['pages'][article_id]['title']
            self.wiki_link = 'http://fr.wikipedia.org/wiki/' + title
        except KeyError:
            wiki_article_intro = "No result"

        return wiki_article_intro

    def get_gmaps_info(self):
        """Gets the information from gmaps about the parsed text, sets googlemaps_response and lng,lat if ok.

        :rtype: string
        """

        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + self.user_message_parsed + "&key=AIzaSyAqlMjGomKCRX2zpADXcv11liLI9H2f1ac"
        resp = requests.get(url)
        data = json.loads(resp.text)
        if data['status'] != 'ZERO_RESULTS':
            self.lat = data['results'][0]['geometry']['location']['lat']
            self.lng = data['results'][0]['geometry']['location']['lng']
            return "OK"
        else :
            self.lng = 0
            self.lat = 0
            return "No result"
#
# def get_wiki_info(input_text):
#     """Gets the 5 first sentences from wikipedia for the article about the parsed text
#
#     :param input_text: The text to parse
#     :type input_text: string
#
#     :rtype: string
#     """
#     api_lnk = 'https://fr.wikipedia.org/w/api.php'
#     api_parm = '?action=query&prop=extracts&exintro&explaintext&format=json&exsentences=5&titles='+input_text
#     json_wiki = json.loads(requests.get(api_lnk+api_parm).text)
#     article_id = list(json_wiki['query']['pages'].keys())[0]
#     try:
#         wiki_article_intro = json_wiki['query']['pages'][article_id]['extract']
#     except KeyError:
#         wiki_article_intro = "No result"
#     return wiki_article_intro
#
