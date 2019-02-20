from pprint import pprint
import requests
import json
import sys
import paho.mqtt.publish as publish
import os
from flask import Flask
from flask import request
import utils

#CHANGE THE TOKEN STRING FOR YOUR BOT'S TOKEN:
bearer = "YjM0Y2JhNjgtMGM5OS00NWFhLWFjZDQtZjk4ZjU1YTkyNDFlMTdlZGY4NWEtNDky" # BOT'S ACCESS TOKEN

def greeting():
    '''
    This is the function to say HI
    '''

    return "Hello, I'm your IOT bot :)"

def lightOn(idNumber):
    '''
    This is the function to turn on the switch
    '''

    publish.single(hostname='',#set the hostname from Heroku MQTT
                   port=, #set the port from Heroku MQTT
                   topic='cmnd/switch'+idNumber+'/power', #this is the topic you will set in Heroku and MQTT channel of the Switch
                   payload='ON',#this is the payload for the topic
                   auth={'username':'','password':''})#this is the credentials for Heroku MQTT
    return "I turned on the switch "+idNumber


def lightOff(idNumber):
    '''
    This is the function to turn off the switch
    '''

    publish.single(hostname='',#set the hostname from Heroku MQTT
                  port= ,#set the port from Heroku MQTT
                  topic='cmnd/switch'+idNumber+'/power',#this is the topic you will set in Heroku and MQTT channel of the Switch
                  payload='OFF',#this is the payload for the topic
                  auth={'username':'','password':''})#this is the credentials for Heroku MQTT
    return "I turned off the switch "+idNumber

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def spark_webhook():
    '''
    Web Server :D
    '''

    #CHANGE THE LAST 4 DIGITS OF YOUR SWITCH HERE (EJ. 83E9)
    switch='83e9'
    '''
    ====================MESSAGES FROM WEBEX TEAMS=======================
    '''
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        if webhook['data']['personEmail']!= bot_email:
            print("MESSAGE FROM "+webhook['data']['personEmail'])
            msg = None

            result = utils.send_spark_get('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
            in_message = result.get('text', '')

            #====================COMMANDS=======================
            if in_message.startswith('Turn on'):
                msg = lightOn(switch)
            elif in_message.startswith('Turn off'):
                msg = lightOff(switch)
            elif in_message.startswith('Hi'):
                msg = greeting()

            else:
                msg = "Sorry, I didn't get that. I respond to 'Hi','Turn on' and 'Turn off'"

            if msg != None:
                utils.send_spark_post("https://api.ciscospark.com/v1/messages",
                                {"roomId": webhook['data']['roomId'], "markdown": msg})
        return "true"
        '''
        =====================MESAGES FROM THE BROWSER=======================
        '''
    elif request.method == 'GET':
        message = "<center><img src=\"http://bit.ly/SparkBot-512x512\" alt=\"WebEx Teams BOT\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>CONGRATULATIONS YOUR BOT <i style=\"color:#ff8000;\">%s</i> is currently online!</b></h2></center>" \
                  "<center><b><i>Now it is time to register your bot with the Webhook so it can start listening your requests</i></b></center>" \
                  "<center><b><a href='https://developer.webex.com/endpoint-webhooks-post.html'>Webhook Registration </a></b></center>"% bot_name
        return message


if __name__ == "__main__":
    global bot_email, bot_name
    if len(bearer) != 0:
        test_auth = utils.send_spark_get("https://api.ciscospark.com/v1/people/me", js=False)
        if test_auth.status_code == 401:
            print("Are you sure this is the right token?")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName","")
            bot_email = test_auth.get("emails","")[0]
            print("Token is valid! Starting!")
    else:
        print("Remember to set the token string in the bearer variable")
        sys.exit()

    #====================BOT INITIALIZATION=======================
    port = int(os.environ.get("PORT", 8080))
    #THHIS PORT WILL BE USED WITH THE IP FROM YOUR COMPUTER WHEN YOU REGISTER THE WEBHOOK
    ip = str(os.environ.get("IP", "0.0.0.0"))
    app.run(host='0.0.0.0', port=port)
