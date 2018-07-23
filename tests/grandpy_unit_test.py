from app.grandpy import BotResponse

def test_parseText():
    bot_response = BotResponse("Bonjour. Comment allez vous ? Parlons de Paris !")
    assert bot_response.user_message_parsed == "bonjour allez parlons paris"

def test_get_wiki_info():
    bot_response = BotResponse("Paris")
    assert bot_response.wiki_response[:90] == "Paris (prononcé [pa.ʁi] ) est la capitale de la France. Elle se situe au cœur d'un vaste b"


def test_get_wiki_info_error():
    # testing wiki response with random string to generate error
    bot_response = BotResponse("dsmjhfqùjhqfm")

    assert bot_response.wiki_response == "No result"


def test_get_gmap_info_error():
    # testing wiki response with random string to generate error
    bot_response = BotResponse("dsmjhfqùjhqfm")
    assert bot_response.gmaps_response == "No result"
    assert bot_response.lat == 0
    assert bot_response.lng == 0

def test_get_gmap_info():
    # testing wiki response with random string to generate error
    bot_response = BotResponse("Paris")
    assert bot_response.gmaps_response == "OK"
    assert bot_response.lat == 48.856614
    assert bot_response.lng == 2.3522219


def test_botresponse():
    bot_response = BotResponse("b")
    assert bot_response.user_message_parsed == ""
    assert bot_response.gmaps_response == "No result"
    assert bot_response.lat == 0
    assert bot_response.lng == 0