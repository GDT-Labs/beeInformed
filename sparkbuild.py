import requests
import json
import base64
import private
import os


def beeColaborative():

	data = {
  		"title" : "ALERT: beeNtouch"
  	}
	headers = {}  # empty dictionary
	headers["Authorization"] = "Bearer " + private.sparkToken
	# Create a new project
	urlString = "https://api.ciscospark.com/v1/rooms"
	r = requests.post(urlString, headers=headers, json=data)
	
	resp = r.json()
	roomID = resp["id"]

	print resp

	r = requests.get("https://api.ciscospark.com/v1/rooms", headers=headers)

	resp = r.json()

	_roomID = roomID
	roomURL = base64.b64decode(roomID)
	roomURL = roomURL[5:]
	print roomURL

	for user in private.users:
		data = {
		  "roomId" : roomID,
		  "personEmail" : user["email"]
		}

		r = requests.post("https://api.ciscospark.com/v1/memberships", headers=headers, json=data)
		resp = r.json()
		print r.status_code

		tropoData = {
			"token": private.tropoToken,
	    	"numberToDial": user["phone"],
	    	"myURL": roomURL
	    }

		tropoHeaders = {}
		tropoHeaders["accept"] = "application/json"
		tropoHeaders["content-type"] = "application/json"

		r = requests.post("https://api.tropo.com/1.0/sessions", headers=tropoHeaders, json=tropoData)

		print "Tropo status:", r.status_code
		print r.text

	print "Done"

	return roomID

def postMessage(message, file, roomID):
	headers = {}  # empty dictionary
	headers["Authorization"] = "Bearer " + private.sparkToken
	headers["Content-Type"] = "application/json; charset=utf-8"

	data = {
	  "roomId" : roomID
	}

	if file == True:
		data['file'] = message
	else:
		data['text'] = message

	print data

	r = requests.post("https://api.ciscospark.com/v1/messages", headers=headers, json=data)

	print r.status_code


if __name__ == "__main__":
	roomID=beeColaborative()
	postMessage("http://i.imgur.com/MCfBbUo.jpg", True, roomID)

