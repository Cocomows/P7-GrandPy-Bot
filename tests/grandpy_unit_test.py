#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.grandpy import BotResponse


def test_parse_text():
    bot_response = BotResponse("Bonjour. Comment allez vous ? Parlons de Paris !")
    assert bot_response.user_message_parsed == "bonjour allez parlons paris"


def test_parse_text_apostrophe():
    bot_response = BotResponse("Gare d'austerlitz")
    assert bot_response.user_message_parsed == "gare austerlitz"


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

