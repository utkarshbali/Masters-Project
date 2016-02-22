from twython import TwythonStreamer

from twython import Twython

import tweepy

import time

import requests

import json





# The consumer key and secret will be generated for you after

consumer_key = "z83IZpYBoW7QQULApvdLAB1Td"
consumer_secret = "HFkUcj2wu8L5P76muXiy7UPJ2bVwq7ejiXGjEt5eRiEyZGX2dn"
# After the step above, you will be redirected to your app's page.

# Create an access token under the the "Your access token" section


access_token="3098250771-WayfyKepH7jux5AKo0jWJYwXcglWNLBRJjcObaE"
access_token_secret="jO00h2y27ymhtT7GcIudA02ymx361WeNFT4bt69cDO1mJ"



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



twitter =  Twython(consumer_key, consumer_secret,

                    access_token, access_token_secret)



f1 = open("usersList.txt","r")
f1.seek(0)
getusers = f1.readlines();

ids=[]

for u in getusers:

    print(u)

    try:

        user =  api.get_user(u)

        ids.append(str(user.id))

    except tweepy.TweepError as e:   
        print(e)
        #print("Error. Waiting....")
        time.sleep(300)

f=file("data.json","w")

class MyStreamer(TwythonStreamer):

    def on_success(self, data):

        global f

        if 'text' in data:
            #print (data['user']['screen_name'].encode('utf-8')+' '+data['text'].encode('utf-8'))
            f.write(json.dumps(data) + "\n")

    def on_error(self, status_code, data):
        print status_code
        pass


stream = MyStreamer(consumer_key, consumer_secret,

                    access_token, access_token_secret)

tweets = stream.statuses.filter(follow=ids,result_type="recent")
