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
import pandas



consumer_key = 'zQnhlYjr2Jzs449ffX32KjesC'
consumer_secret = 'z4e50oEBrBSFBklXZkAwUpfQ1bMkdzcDYgzrnNNEYcKhbIk5PC'
access_token = '449638146-81zTSVFCKrqz2ZqCtbsUg9S3q5fC5eekpm3NknY9'
access_secret = 'xTQOdtxNgGg9ciYntAqrU6cJ8HbKnjuuxz08hGNOvHuNo'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#nltk.download()
punctuation = list(string.punctuation)
print(punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'the', 'amp', 'also', 'said', '.', ',', '...']
count_all = Counter()
dates_angry = []


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
    r'["][a-zA-Z0-9]+["]', #...
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"""(?:[a-z][a-z'\-_]+[a-z])""",  # words with - and '

    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

def getFrequencyGraph(word_freq):
    labels, freq = zip(*word_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.to_json('term_freq.json')

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

for status in tweepy.Cursor(api.user_timeline, id="@realdonaldtrump").items(20):
    # Process a single status
    i = i+1
    preprocess(status.text.lower())
    print(count_all.most_common(20))
    getFrequencyGraph(count_all.most_common(20))
    print("******")