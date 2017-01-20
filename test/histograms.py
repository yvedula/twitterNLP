import string

import tweepy
import nltk
from tweepy import OAuthHandler
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams
from nltk import collocations
import re
import operator
import json
from collections import Counter
import vincent
import numpy as np
import matplotlib.pyplot as plt
from test import settings


consumer_key = settings.consumer_key
consumer_secret = settings.consumer_secret
access_token = settings.access_token
access_secret = settings.access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#nltk.download()
punctuation = list(string.punctuation)
print(punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'the', 'amp', 'also', 'said', '.', ',']
count_all = Counter()

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
    r'[A-Z][.][A-Z][.]?', #U.S or U.S.
    r'[0-9]+th', #Dates, like 5th
    r'[0-9]+rd', #Dates, like 3rd
    r'[0-9]+st', #Dates, like 1st
    r'[0-9]+nd', #Dates, like 2nd
    r'[.,!]+', #...
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"""(?:[a-z][a-z'\-_]+[a-z])""",  # words with - and '
    r"""(?:[a-z][a-z"\-_]+[a-z])""",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

def getFrequencyGraph(word_freq):
    labels, freq = zip(*word_freq)
    data = {'data': freq, 'x': labels}

    indexes = np.arange(len(labels))
    width = 0.7

    plt.bar(indexes, freq, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()
    # bar = vincent.Bar(data, iter_idx='x')
    # bar.to_json('term_freq.json')



def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    #count_all.clear()
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) and token else token.lower() for token in tokens]
    for word in stop:
        if word in tokens:
            tokens.remove(word)
    count_all.update(tokens)
    return tokens
i = 0
#print (stop)

def getBigrams(s):
    count_all.clear()
   # print(preprocess(s))
    terms_bigram = list(bigrams(preprocess(s)))
    #print(terms_bigram)
    count_all.update(terms_bigram)
    print(count_all.most_common(10))


tweets = []
tweets2 = []
for status in tweepy.Cursor(api.user_timeline, id="@realdonaldtrump").items(5):
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

    i = i-1
print(tweets2)
#getFrequencyGraph(count_all.most_common(20))
