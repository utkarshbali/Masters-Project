from twython import TwythonStreamer

from twython import Twython

from requests.exceptions import ChunkedEncodingError

import tweepy

import time

import requests

import json





# The consumer key and secret will be generated for you after

consumer_key = "XaA0NXj1G6xeKPcqnlRqxzjNa"
consumer_secret = "O6GU85y5uuMTwhyhIda1lFpfsuUoXRUlDJCzauTScr7lmNtNJo"
# After the step above, you will be redirected to your app's page.

# Create an access token under the the "Your access token" section


access_token="3098250771-86hPD5eY4de23dprtYhGaQ8e3dlhIGrHAO9HywX"
access_token_secret="xRIpoga9jfbviU3YFreRM1Sx4458ERTpgAZIX9p6dbyXw"



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



twitter =  Twython(consumer_key, consumer_secret,

                    access_token, access_token_secret)


f=file("nonRocData-03-2016.json","w")

class MyStreamer(TwythonStreamer):

    def on_success(self, data):

        global f

        if 'text' in data:          

            #print (data['user']['screen_name'].encode('utf-8')+' '+data['text'].encode('utf-8'))

            f.write(json.dumps(data) + "\n")
            time.sleep(3)
    
    def on_error(self, status_code, data):
        print status_code
        pass

def streamNonRocTweets():
    while True:
        try:
            stream = MyStreamer(consumer_key, consumer_secret,access_token, access_token_secret)
            tweets = stream.statuses.filter(locations=[-125.0011, 24.9493, -66.9326, 49.5904])
        except ChunkedEncodingError:
            continue

streamNonRocTweets()