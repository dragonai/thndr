import re

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

from twilio import twiml
from twilio.util import TwilioCapability

from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'x'
google_places = GooglePlaces(YOUR_API_KEY)



# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')

# Voice Request URL
@app.route('/voice', methods=['GET', 'POST'])
def voice():
    response = twiml.Response()
#    response.say("Hi there. Please shoot us a text with what you're looking" \
#            " for and where you're looking for it.")
    response.play("http://a.tumblr.com/tumblr_mcuje2x1TR1rhztipo1.mp3")
    return str(response)


# SMS Request URL
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    response = twiml.Response()
    body = request.form['Body']
    ##some ghetto, hackathon-level NLP going on here
    if "fox say" in body:
        response.sms("Go away.")
        return str(response)
    first = 0;
    if "Best" in body:
        first = body.find("Best") + 5
    if "best" in body:
        first = body.find("best") + 5
    last = 0
    if " in " in body:
        last = body.find(" in ")
    if " near " in body:
        last = body.find(" near ")
    if " at " in body:
        last = body.find(" at ")    

    item = body[first:last]
    
    loc = 0
    if " in " in body:
        loc = body.find(" in ") + 4
    if " near " in body:
        loc = body.find(" near ") + 6
    if " at " in body:
        loc = body.find(" at ") + 4
    query_result = google_places.nearby_search(
        location=body[loc:], keyword=item,
        radius=16000, types=[types.TYPE_FOOD])
    x = 0
        #y = 0
    best = ""
    addy = ""
        #secondbest = ""
    for place in query_result.places:
        if place.rating > x:
            x = place.rating
            best = place.name
            place.get_details()
            addy = place.formatted_address
            #if (place.rating > y) and (place.rating < x)
            #    y = place.rating
            #    secondbest = place.name
    if(best == "") or (addy == ""):
        response.sms("Ah crap. It seems Thndr couldn't locate a good place for ya. Try a different search, perhaps?")
        return str(response)
    response.sms("Thndr suggests " + best + ". It's located at " + addy + ".")
    return str(response)

# Twilio Client demo template
@app.route('/client')
def client():
    configuration_error = None
    for key in ('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_APP_SID',
            'TWILIO_CALLER_ID'):
        if not app.config[key]:
            configuration_error = "Missing from local_settings.py: " \
                    "%s" % key
            token = None

    if not configuration_error:
        capability = TwilioCapability(app.config['TWILIO_ACCOUNT_SID'],
            app.config['TWILIO_AUTH_TOKEN'])
        capability.allow_client_incoming("joey_ramone")
        capability.allow_client_outgoing(app.config['TWILIO_APP_SID'])
        token = capability.generate()
    params = {'token': token}
    return render_template('client.html', params=params,
            configuration_error=configuration_error)

@app.route('/client/incoming', methods=['POST'])
def client_incoming():
    try:
        from_number = request.values.get('PhoneNumber', None)

        resp = twiml.Response()

        if not from_number:
            resp.say(
                "Your app is missing a Phone Number. "
                "Make a request with a Phone Number to make outgoing calls with "
                "the Twilio hack pack.")
            return str(resp)

        if 'TWILIO_CALLER_ID' not in app.config:
            resp.say(
                "Your app is missing a Caller ID parameter. "
                "Please add a Caller ID to make outgoing calls with Twilio Client")
            return str(resp)

        with resp.dial(callerId=app.config['TWILIO_CALLER_ID']) as r:
            # If we have a number, and it looks like a phone number:
            if from_number and re.search('^[\d\(\)\- \+]+$', from_number):
                r.number(from_number)
            else:
                r.say("We couldn't find a phone number to dial. Make sure you are "
                      "sending a Phone Number when you make a request with Twilio "
                      "Client")

        return str(resp)

    except:
        resp = twiml.Response()
        resp.say("An error occurred. Check your debugger at twilio dot com "
                 "for more information.")
        return str(resp)


# Installation success page
@app.route('/')
def index():
    params = {
        'Voice Request URL': url_for('.voice', _external=True),
        'SMS Request URL': url_for('.sms', _external=True),
        'Client URL': url_for('.client', _external=True)}
    return render_template('index.html', params=params,
            configuration_error=None)

