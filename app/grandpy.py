#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module used for GrandPy Bot
Stopword list used from https://github.com/stopwords-iso/stopwords-fr/blob/master/stopwords-fr.json
"""
import json
import os
import requests
import re
from config import GMAPS_API_KEY


class BotResponse:

    def __init__(self, user_message):
        # Adding space before and after message for parsing.
        self.user_message = user_message
        self.user_message_parsed = self.parse_text()
        self.name = "No result"
        self.address = "No result"
        self.wiki_response_html = "Je n'ai pas compris la demande ou je ne connais pas d'histoire à ce sujet."
        self.wiki_json = ''
        self.gmaps_response = "No result"
        self.gmaps_json = ''

        if self.user_message_parsed != "":
            self.wiki_response_html = self.get_wiki_info()
            self.gmaps_response = self.get_gmaps_info()

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


        # Remove all punctuation and make text lowercase with a regex

        string_no_punctuation = re.sub(r"[-,.;@#?!&$']+ *", " ", self.user_message.lower(), )

        words_to_parse = string_no_punctuation.split()
        resultwords = []

        for word in words_to_parse:
            if word not in stopwords:
                resultwords.append(word)
        parsed_text = ' '.join(resultwords)

        return parsed_text

    def get_wiki_info(self):
        """Gets the 5 first sentences from wikipedia for the article about the parsed text

        :rtype: string
        """
        search_term = self.user_message_parsed
        api_url = 'https://fr.wikipedia.org/w/api.php'
        payload = {'action': 'query',
                   'prop': 'extracts',
                   'exintro': 1,
                   'explaintext': 1,
                   'format': 'json',
                   'indexpageids': 1,
                   'exsentences': 5,
                   'generator': 'search',
                   'gsrlimit': 1,
                   'gsrsearch': search_term,

                   }

        resp = requests.get(api_url, params=payload)
        self.wiki_json = json.loads(resp.text)

        try:
            article_id = self.wiki_json ['query']['pageids'][0]
            wiki_article_intro = self.wiki_json['query']['pages'][article_id]['extract']
            wiki_link = 'http://fr.wikipedia.org/?curid='+article_id
            wiki_article_intro = wiki_article_intro + ' <a href="' + \
                                 wiki_link + '" target="_blank">En savoir plus sur wikipédia.</a>'

        except KeyError:
            wiki_article_intro = self.wiki_response_html

        return wiki_article_intro

    def get_gmaps_info(self):
        """Gets the information from gmaps about the parsed text, sets googlemaps_response and lng,lat if ok.

        :rtype: string
        """

        search_term = self.user_message_parsed
        api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

        payload = {'key': GMAPS_API_KEY,
                   'inputtype': 'textquery',
                   'locationbias': 'point:48.856614,2.3522219',
                   'language': 'fr',
                   'input': search_term,
                   'type': 'street_address',
                   'fields': 'formatted_address,geometry,name,place_id',
                   }

        resp = requests.get(api_url, params=payload)
        data = json.loads(resp.text)

        self.gmaps_json = data
        print(resp.url)
        print(self.gmaps_json)

        if data['status'] != 'ZERO_RESULTS':
            try:
                self.name = data['candidates'][0]['name']
                self.address = data['candidates'][0]['formatted_address']
            except IndexError:
                return "No result"
            return "OK"
        else:
            return "No result"



