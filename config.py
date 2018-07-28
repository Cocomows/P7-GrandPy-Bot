import os

if os.environ.get('IS_HEROKU', None) :
    GMAPS_API_KEY = os.environ.get('GMAPS_API_KEY')
else:
    from api_key_local import GMAPS_KEY
    GMAPS_API_KEY = GMAPS_KEY
