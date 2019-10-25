import os
import sys
import json
import sqlite3
from datetime import datetime
import time
import requests
from flask import Flask, request

point =0
arrA = [0,0,0,0,0,0,0]
arrB = [0,0,0,0,0,0,0]


app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
def readanl(filepath):
    with open(filepath,'r') as analysis :
        file = analysis.read()
    return file

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
	db =DBHelper()
	db.setup()
	data = request.get_json()
	log(data)  # you may not want to log every incoming message in production, but it's good for testing


	if data["object"] == "page":

		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:
			
				tmp = readanl("question.txt")
				q = tmp.split('$')

				if messaging_event.get("message"):  # someone sent us a message

					sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
					
					
					recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
				
					message_text = messaging_event["message"]["text"]  # the message's text
					#id =db.get_items(sender_id)
					global point
					#if not id:
						#db.add_item(sender_id,0)
					#else:
						#x=id[0]
						#point = int(x)+1
						#db.delete_item(sender_id,point )
						
						
					
					global arrA
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
						send_final_message(sender_id, "Your Result IS : "+qp[ind])
						return "ok", 200
					if(message_text == "A"):
						arrA[point%7] += 1;
					if(message_text=="B"):
						arrB[point%7] +=1
					send_message(sender_id,q[point] )
					point = point +1
					time.sleep(1)
					

					#send_message(sender_id, "roger that!")

				if messaging_event.get("delivery"):  # delivery confirmation
					pass

				if messaging_event.get("optin"):  # optin confirmation
					pass

				if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
					pass

	return "ok", 200


def send_message(recipient_id, message_text):

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


def send_final_message(recipient_id, message_text):

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
            "text": message_text 
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

	
class DBHelper:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (id text , count int)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, fid,count):
        stmt = "INSERT INTO items (id,count) VALUES (?,?)"
        args = (fid,count )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text,c):
        stmt = "UPDATE items SET count = (?) WHERE id = (?)"
        args = (item_text,c )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, fid):
        stmt = "SELECT count FROM items WHERE id = (?)"
        args = (fid, )
        return [x[0] for x in self.conn.execute(stmt, args)]
		
	def update_item(self, fid,count):
		stmt = "UPDATE items SET count = (?) WHERE id = (?)"
		args = (count,fid )
		self.conn.execute(stmt, args)
		self.conn.commit()


if __name__ == '__main__':
    app.run(debug=True)
