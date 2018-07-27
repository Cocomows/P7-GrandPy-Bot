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


class BotResponse:

    def __init__(self, user_message):
        self.user_message = user_message+" "
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

        parsed_text = re.sub(r"[-,.;@#?!&$']+ *", " ", self.user_message.lower(), )

        # Remove stopwords and extra space
        for word in parsed_text.split():
            if word in stopwords:
                parsed_text = parsed_text.replace(word+" ", "", 1)
            parsed_text = " ".join(parsed_text.split())
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
            wiki_article_intro = self.wiki_json ['query']['pages'][article_id]['extract']
            title = self.wiki_json ['query']['pages'][article_id]['title']
            wiki_link = 'http://fr.wikipedia.org/wiki/' + title
            wiki_article_intro = wiki_article_intro+ ' <a href="' + \
                                 wiki_link + '" target="_blank">En savoir plus sur wikipédia.</a>'

        except KeyError:
            wiki_article_intro = "Je n'ai pas compris la demande ou je ne connais pas d'histoire à ce sujet."

        return wiki_article_intro

    def get_gmaps_info(self):
        """Gets the information from gmaps about the parsed text, sets googlemaps_response and lng,lat if ok.

        :rtype: string
        """

        search_term = self.user_message_parsed
        api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        payload = {'key': 'AIzaSyAqlMjGomKCRX2zpADXcv11liLI9H2f1ac',
                   'inputtype': 'textquery',
                   'locationbias': 'ipbias',
                   'input': search_term,
                   'fields': 'formatted_address,geometry,name,place_id',
                   }

        resp = requests.get(api_url, params=payload)
        data = json.loads(resp.text)

        self.gmaps_json = data
        if data['status'] != 'ZERO_RESULTS':
            self.name = data['candidates'][0]['name']
            self.address = data['candidates'][0]['formatted_address']
            return "OK"
        else:
            return "No result"
