from flask import Flask, render_template, request, jsonify
from .grandpy import BotResponse
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("pages/home.html")


@app.route('/_response', methods=['POST'])
def response():
    bot_response = BotResponse(request.form['user_message'])
    print(bot_response.user_message_parsed)
    wiki_reply = bot_response.wiki_response_html
    gmap_reply = bot_response.gmaps_response

    gmaps_address = bot_response.address
    gmaps_name = bot_response.name
    gmaps_json = bot_response.gmaps_json

    return jsonify(wiki_reply=wiki_reply, gmaps_reply=gmap_reply, gmaps_address=gmaps_address,
                   gmaps_name=gmaps_name, gmaps_json=gmaps_json)


@app.route('/about')
def about():
    return render_template("pages/about.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
