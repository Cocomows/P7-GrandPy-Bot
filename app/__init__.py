from flask import Flask, render_template, request, jsonify
from grandpy import BotResponse,get_wiki_info
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("pages/home.html")

@app.route('/_response', methods=['POST'])
def response():
    bot_response = BotResponse(request.form['user_message'])

    #
    # message = request.form['user_message']
    # print(message)
    # parsed_Text = parse_text(message)

    # reply = "Mots retenus dans le message : '"+parsed_Text+"'"
    wiki_reply = get_wiki_info(bot_response.user_message_parsed)
    gmaps_reply_lng = ""
    gmaps_reply_lat = ""
    return jsonify(wiki_reply=wiki_reply, gmaps_reply_lat=gmaps_reply_lat, gmaps_reply_lng=gmaps_reply_lng, consolemsg="ok")

@app.route('/about')
def about():
    return render_template("pages/about.html")

@app.route('/maps')
def maps():
    return render_template("pages/maps_api_test.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)