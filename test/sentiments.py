import json
import tweepy
from tweepy import OAuthHandler
from watson_developer_cloud import AlchemyLanguageV1
from test import settings



consumer_key = settings.consumer_key
consumer_secret = settings.consumer_secret
access_token = settings.access_token
access_secret = settings.access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def analyze_tweet(tweet):
    alchemy_language = AlchemyLanguageV1(api_key=settings.alchemyKey)
    unparsed_json = json.dumps(
      alchemy_language.combined(
        text=tweet,
        extract='keywords',
        sentiment=1),
      indent=2)

    parsed_json = json.loads(unparsed_json)
    #print(unparsed_json)
    length = len(parsed_json['keywords'])
    for keyword in parsed_json['keywords']:
        print(keyword['text'] + " : " + keyword['sentiment']['type'])
        print('---')

i = 0
tweets = []
tweets2 = []
for status in tweepy.Cursor(api.user_timeline, id="@realdonaldtrump").items(10):
    # Process a single status
    i = i+1

    s = status.text
    tweets.append(s)

i = len(tweets)-1
temp = ""
while i >=0:
    s = tweets[i]
    temp = tweets[i]
    if s.endswith(".."):
        while tweets[i].endswith(".."):
            temp = temp[0:tweets[i].index("..")]+" " + tweets[i-1]
            i = i-1
    #print(temp)

    tweets2.append(temp)
    print(temp)
    analyze_tweet(temp)
    print("**********")
    i = i-1

#analyze_tweet("Getting ready to leave for Washington, D.C. The journey begins and I will be working and fighting very hard to make it a great journey for the American people. I have no doubt that we will, together, MAKE AMERICA GREAT AGAIN!")
#print(tweets2)


