from __future__ import print_function
import random

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

def joke_response():
    jokes=[
        "What do you get when you wake up on a workday and realize you ran out of coffee?-a depresso",
        "My dog is an awesome fashion adviser. Every time I ask him what I look like in my clothes, he says WOW!",
        "Why are eggs not very much into jokes? Because they could crack up"
        ]
    session_attributes = {}
    card_title = "jokes"
    speech_output = random.choice(jokes)
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))





def get_welcome_response():
   
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to my fact and joke application"
    reprompt_text = "Welcome to my fact and joke application"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
   
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
   
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
   
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "jokeIntent":
        return joke_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
   
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])



def lambda_handler(event, context): 
   
    print("Incoming request...")

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
