from app.grandpy import BotResponse

def test_parseText():
    bot_response = BotResponse("Bonjour. Comment allez vous ? Parlons de Paris !")
    parsed_text = bot_response.user_message_parsed
    assert parsed_text == "bonjour allez parlons paris"

