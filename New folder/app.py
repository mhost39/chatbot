#Python libraries that we need to import for our bot
import random
import json
import sys
import time
import requests
from flask import Flask, request
from pymessenger.bot import Bot
import os 
from datetime import datetime
app = Flask(__name__)
ACCESS_TOKEN = 'EAAGPoHq4OpABAIrwcpEC7pBICzgbxh8aZBOSKjj7tcSBHzmWmwtvRbdvubtisK1nOXImzjZAe88cCjCZCdEk6oUgzSs5YX9Gpu3F3w770GGkNIbpscdxJlpdGS6gBDgI2ZB6gMiMibmQHrkT2qrLG2iHpnqs578NGQqcm0Du0XMKMfkVOGOc'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'mhost132'   #VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)
hassan = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
def readanl(filepath):
    with open(filepath,'r') as analysis :
        file = analysis.read()
    return file


point =0
arrA = [0,0,0,0,0,0,0]
arrB = [0,0,0,0,0,0,0]

hashArr = {'ISTJ':0,'ISFJ':1,'INFJ':2,'INTJ':3,'ISTP':4,'ISFP':5,'INFP':6,'INTP':7,'ESTP':8,'ESFP':9,'ENFP':10,'ENTP':11,'ESTJ':12,'ESFJ':13,'ENFJ':14,'ENTJ':15}
tmp = readanl("question.txt")
q = tmp.split('$')
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])



def receive_message():
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message(message['message']['text'])
                    send_message(recipient_id, response_sent_text)
                    send_me(recipient_id,"choose")
                   
                    
           
    return "Message Processed"
   # if request.method == 'GET':
        #"""Before allowing people to message your bot, Facebook has implemented a verify token
        #hat confirms all requests that your bot receives came from Facebook.""" 
        #token_sent = request.args.get("hub.verify_token")
        #return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    #else:
        # get whatever message a user sent the bot
  


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(message_text):
    global arrA
    global point
    global arrB
    global hashArr
    if(point == 21):
        arrA[2]+=arrA[1]
        arrB[2]+=arrB[1]
        arrA[4]+=arrA[3]
        arrB[4]+=arrB[3]
        arrA[6]+=arrA[5]
        arrB[6]+=arrB[5]
        s1=s2=s3=s4 =""
        if(arrA[0]>arrB[0]):
            s1="E"
        else:
            s1="I"
        if(arrA[2]>arrB[2]):
            s2="S"
        else:
            s2="N"
        if(arrA[4]>arrB[4]):
            s3="T"
        else:
            s3="F"
        if(arrA[6]>arrB[6]):
            s4="J"
        else:
            s4="P"
        k = s1+s2+s3+s4
        ind = hashArr[k]
        t = readanl("result.txt")
        qp = t.split('$')
        return "Your Result IS : "+qp[ind]
    #sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    if(message_text == "A"):
        arrA[point%7] += 1;
    if(message_text=="B"):
        arrB[point%7] +=1
    
    return q.pop(0)
   
	
    #return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"
	

def send_me(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
     "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text ,
			"quick_replies":[
				{
					"content_type":"text",
					"title":"A",
					"payload":"<POSTBACK_PAYLOAD>",
					
				},
     
				{
					"content_type":"text",
					"title":"B",
					"payload":"<POSTBACK_PAYLOAD>"
				}
			]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == "__main__":
    app.run()
