#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.grandpy import BotResponse

import json
import requests


class MockRequestsResponse:
    def __init__(self, resp):
        self.text = resp
        self.url = "mock_url"


def test_requests_response(monkeypatch):

    results_wiki = '{"batchcomplete":"","continue":{"gsroffset":1,"continue":"gsroffset||"},"query":{"pageids":["681159"],"pages":{"681159":{"pageid":681159,"ns":0,"title":"Paris","index":1,"extract":"Paris (prononc\u00e9 [pa.\u0281i] ) est la capitale de la France. Elle se situe au c\u0153ur d\'un vaste bassin s\u00e9dimentaire aux sols fertiles et au climat temp\u00e9r\u00e9, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l\'Oise. Ses habitants s\u2019appellent les Parisiens. Paris est \u00e9galement le chef-lieu de la r\u00e9gion \u00cele-de-France et l\'unique commune fran\u00e7aise qui est en m\u00eame temps un d\u00e9partement. Commune centrale de la m\u00e9tropole du Grand Paris, cr\u00e9\u00e9e en 2016, elle est divis\u00e9e en arrondissements, comme les villes de Lyon et de Marseille, au nombre de vingt."}}}}'
    results_gmaps = '{"candidates": [ { "formatted_address": "Paris, France", "geometry": { "location": {  "lat": 48.856614,  "lng": 2.3522219 }, "viewport": {  "northeast": {  "lat": 48.9021449,  "lng": 2.4699208  },  "southwest": {  "lat": 48.815573,  "lng": 2.224199  } } }, "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png", "name": "Paris", "place_id": "ChIJD7fiBh9u5kcRYJSMaMOCCwQ" } ], "debug_log": { "line": [] }, "status": "OK"}'

    def mockreturn(api_url, params):
        response = ""
        if api_url == 'https://fr.wikipedia.org/w/api.php':
            response = MockRequestsResponse(results_wiki)
        if api_url == 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json':
            response = MockRequestsResponse(results_gmaps)
        return response

    monkeypatch.setattr(requests, 'get', mockreturn)

    bot_response = BotResponse("paris")

    assert bot_response.wiki_json == json.loads(results_wiki)
    assert bot_response.gmaps_json == json.loads(results_gmaps)


def test_parse_text():
    bot_response = BotResponse("Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?")
    assert bot_response.user_message_parsed == "adresse openclassrooms"


def test_parse_text_apostrophe():
    bot_response = BotResponse("Gare d'austerlitz")
    assert bot_response.user_message_parsed == "gare austerlitz"

def test_parse_repetition():
    bot_response = BotResponse("Parle moi de la grande muraille de chine")
    assert bot_response.user_message_parsed == "grande muraille chine"


def test_get_wiki_info():
    bot_response = BotResponse("Paris")
    assert bot_response.wiki_response_html[:90] == "Paris (prononcé [pa.ʁi] ) est la capitale de la France. Elle se situe au cœur d'un vaste b"


def test_get_wiki_info_error():
    # testing wiki response with random string to generate error
    bot_response = BotResponse("dsmjhfqùjhqfm")
    assert bot_response.wiki_response_html == "Je n'ai pas compris la demande ou je ne connais pas d'histoire à ce sujet."


def test_get_gmap_info_error():
    # testing wiki response with random string to generate error
    bot_response = BotResponse("dsmjhfqùjhqfm")
    assert bot_response.gmaps_response == "No result"


def test_get_gmap_info():
    # testing wiki response with random string to generate error
    bot_response = BotResponse("Paris")
    assert bot_response.gmaps_response == "OK"
    assert bot_response.gmaps_json['candidates'][0]['geometry']['location']['lat'] == 48.856614
    assert bot_response.gmaps_json['candidates'][0]['geometry']['location']['lng'] == 2.3522219


def test_botresponse():
    bot_response = BotResponse("b")
    assert bot_response.user_message_parsed == ""
    assert bot_response.gmaps_response == "No result"

