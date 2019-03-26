"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import crawler
global ses_att
ses_att = {}

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
	return {
		'outputSpeech': {
			'type': 'PlainText',
			'text': output
		},
		'card': {
			'type': 'Simple',
			'title': "SessionSpeechlet - " + title,
			'content': "SessionSpeechlet - " + output
		},
		'reprompt': {
			'outputSpeech': {
				'type': 'PlainText',
				'text': reprompt_text
			}
		},
		'shouldEndSession': should_end_session
	}


def build_response(session_attributes, speechlet_response):
	return {
		'version': '1.0',
		'sessionAttributes': session_attributes,
		'response': speechlet_response
	}


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
	""" If we wanted to initialize the session to have some attributes we could
	add those here
	"""
	speech_output = "Welcome to the Aflexa, your personal William and Mary services assistant. " \
					"Would you like to check your flex or express balance, meal swipes, or laundry machines?"
	#session_attributes = {"expBal": "1", "flexBal": "1", "swipesBal": "1"}
	try:
		crawl = crawler.Crawler()
		try:
			crawl.login("USERNAME","PASSWORD")
		except(AssertionError):
			try:
				crawl.login("USERNAME","PASSWORD")
			except(AssertionError):
				speech_output = "Failed to connect to CBORD, check internet connection?"
		data = crawl.checkCash()
		laundry = crawl.checkLaundry()
		expBal = data[0]
		flexBal = data[1]
		swipesBal = data[2]
		#laundryInfo = crawl.checkLaundry()
	except Exception as e:
		speech_output = str(e)
	try:
		session_attributes = {"expBal": expBal, "flexBal": flexBal, "swipesBal": swipesBal, "laundryData": laundry}
						  #Exp	   #Flex	#Swipes
		ses_att.update({"expBal": expBal, "flexBal": flexBal, "swipesBal": swipesBal, "laundryData": laundry})
	except Exception as e:
		speech_output = str(e)
	card_title = "Welcome"
	
	# If the user either does not reply to the welcome message or says something
	# that is not understood, they will be prompted again with this text.
	reprompt_text = "Would you like to check your flex or express balance, meal swipes, or laundry machines?"
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
	card_title = "Session Ended"
	speech_output = "Thank you for using Aflexa. " \
					"Have a nice day! "
	# Setting this to true ends the session and exits the skill.
	should_end_session = True
	return build_response({}, build_speechlet_response(
		card_title, speech_output, None, should_end_session))

def get_flex_from_session(intent, session):
	session_attributes = ses_att
	reprompt_text = None
	if session.get('attributes', {}) and "flexBal" in session.get('attributes', {}):
		flex_bal = session['attributes']['flexBal']
		speech_output = "Your flex balance is " + str(flex_bal)
		should_end_session = False
	else:
		speech_output = "I'm not sure what your flex balance is. "
		should_end_session = True

	# Setting reprompt_text to None signifies that we do not want to reprompt
	# the user. If the user does not respond or says something that is not
	# understood, the session will end.
	return build_response(session_attributes, build_speechlet_response(
		intent['name'], speech_output, reprompt_text, should_end_session))

def get_expbal_from_session(intent, session):
	session_attributes = ses_att
	reprompt_text = None

	if session.get('attributes', {}) and "expBal" in session.get('attributes', {}):
		exp_bal = session['attributes']['expBal']
		speech_output = "Your express balance is " + str(exp_bal)
		should_end_session = False

	else:
		speech_output = "I'm not sure what your express balance is. "
		should_end_session = True

	# Setting reprompt_text to None signifies that we do not want to reprompt
	# the user. If the user does not respond or says something that is not
	# understood, the session will end.
	return build_response(session_attributes, build_speechlet_response(
		intent['name'], speech_output, reprompt_text, should_end_session))

def get_swipes_from_session(intent, session):
	session_attributes = ses_att
	reprompt_text = None

	if session.get('attributes', {}) and "swipesBal" in session.get('attributes', {}):
		swipes_bal = session['attributes']['swipesBal']
		speech_output = "You have " + str(swipes_bal) + " swipes left."
		should_end_session = False
	else:
		speech_output = "I'm not sure what your meal swipe balance is. "
		should_end_session = True


	# Setting reprompt_text to None signifies that we do not want to reprompt
	# the user. If the user does not respond or says something that is not
	# understood, the session will end.
	return build_response(session_attributes, build_speechlet_response(
		intent['name'], speech_output, reprompt_text, should_end_session))

def set_location_from_session(intent, session):
	card_title = intent['Name']
	session_attributes = ses_att
	reprompt_text = None
	if 'Floor' in intent['slots']:
		locationInfo = intent['slots']['Floor']['value']
		ses_att.update({"locationInfo": locationInfo})
		speech_output = "Please ask about your laundry again."
		should_end_session = False
	else:
		speech_output = "That's not a location in that building."
		should_end_session = True

	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))

def set_dorm_from_session(intent, session):
	card_title = intent['Name']
	session_attributes = ses_att
	reprompt_text = None
	try:
		if 'Dorm' in intent['slots']:
			dormInfo = intent['slots']['Dorm']['value']
			ses_att.update({"dormInfo":dormInfo})
			speech_output = "Now choose a laundry room in that building."
			should_end_session = False
		else:
			speech_output = "That's not a building."
			should_end_session = True
	except Exception as e:
		speech_output = str(e)
		should_end_session = True
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))

def get_big_boy_from_session(intent, session):
	session_attributes = ses_att
	reprompt_text = ""
	speech_output = ""
	try:
		crawl = crawler.Crawler()
		results = crawl.getLaundryData(session_attributes['laundryData'], "")
		for result in results:
			speech_output = speech_output + result[0] + " has " + result[1] + " washers " + result[2] + " dryers available. "
	except Exception as e:
		speech_output = str(e)
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))

def get_laundry_from_session(intent, session):
	session_attributes = ses_att
	reprompt_text = ""
	speech_output = ""
	should_end_session = False
	if session.get('attributes', {}) and "laundryData" in session.get('attributes', {}):
		if 'Dorm' in intent['slots']:
			crawl = crawler.Crawler()
			dorm = intent['slots']['Dorm']['value']
			results = crawl.getLaundryData(session_attributes['laundryData'], dorm)
			for result in results:
				speech_output = speech_output + result[0] + " has " + result[1] + " washers " + result[2] + " dryers available. "
		else:
			speech_output = "Please say the name of a valid building"
			reprompt_text = "Please specify the dorm and try again"
	else:
		speech_output = "Failed"
		should_end_session = False
	should_end_session = False
	#dorm = intent['slots']['Dorm']['value']
		#try:
	#		location = intent['slots']['Floor']['value']
	#	except:
	#		location = None
	#	if(location is None):
	#		laundry_info = crawler.getLaundryData(session_attributes['laundryData'], dorm)
	#	else:
	#		laundry_info = crawler.getLaundryData(session_attributes['laundryData'], dorm, location)
	#	if len(laundry_info[0])==0:
	#		speech_output = "This location was not found, try again with a valid location"
	#	else:
	#		speech_output = str(laundry_info[0][0]) + "has " + str(laundry_info[0][1]) + " washers and " + str(laundry_info[0][2]) + " dryers available."
	#	should_end_session = False



	# Setting reprompt_text to None signifies that we do not want to reprompt
	# the user. If the user does not respond or says something that is not
	# understood, the session will end.
	return build_response(session_attributes, build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))
# --------------- Events ------------------

def on_session_started(session_started_request, session):
	""" Called when the session starts """

	print("on_session_started requestId=" + session_started_request['requestId']
		  + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
	""" Called when the user launches the skill without specifying what they
	want
	"""

	print("on_launch requestId=" + launch_request['requestId'] +
		  ", sessionId=" + session['sessionId'])
	# Dispatch to your skill's launch
	return get_welcome_response()


def on_intent(intent_request, session):
	""" Called when the user specifies an intent for this skill """

	print("on_intent requestId=" + intent_request['requestId'] +
		  ", sessionId=" + session['sessionId'])

	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']

	# Dispatch to your skill's intent handlers
	if intent_name == "WhatsMyExpressIntent":
		return get_expbal_from_session(intent, session)
	elif intent_name == "WhatsMyFlexIntent":
		return get_flex_from_session(intent, session)
	elif intent_name == "SwipesIntent":
		return get_swipes_from_session(intent, session)
	elif intent_name == "LaundryIntent":
		return get_laundry_from_session(intent, session)
	elif intent_name == "BigIntent":
		return get_big_boy_from_session(intent, session)
	#elif intent_name == "BuildingIntent":
	#	return set_dorm_from_session(intent, session)
	#elif intent_name == "FloorIntent":
	#		return set_location_from_session(intent, session)
	elif intent_name == "AMAZON.HelpIntent":
		return get_welcome_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()
	else:
		raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
	""" Called when the user ends the session.

	Is not called when the skill returns should_end_session=true
	"""
	print("on_session_ended requestId=" + session_ended_request['requestId'] +
		  ", sessionId=" + session['sessionId'])
	# add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
	""" Route the incoming request based on type (LaunchRequest, IntentRequest,
	etc.) The JSON body of the request is provided in the event parameter.
	"""
	print("event.session.application.applicationId=" +
		  event['session']['application']['applicationId'])

	"""
	Uncomment this if statement and populate with your skill's application ID to
	prevent someone else from configuring a skill that sends requests to this
	function.
	"""
	# if (event['session']['application']['applicationId'] !=
	#		  "amzn1.echo-sdk-ams.app.[unique-value-here]"):
	#	  raise ValueError("Invalid Application ID")

	if event['session']['new']:
		on_session_started({'requestId': event['request']['requestId']},
						   event['session'])

	if event['request']['type'] == "LaunchRequest":
		return on_launch(event['request'], event['session'])
	elif event['request']['type'] == "IntentRequest":
		return on_intent(event['request'], event['session'])
	elif event['request']['type'] == "SessionEndedRequest":
		return on_session_ended(event['request'], event['session'])
