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



consumer_key = 'zQnhlYjr2Jzs449ffX32KjesC'
consumer_secret = 'z4e50oEBrBSFBklXZkAwUpfQ1bMkdzcDYgzrnNNEYcKhbIk5PC'
access_token = '449638146-81zTSVFCKrqz2ZqCtbsUg9S3q5fC5eekpm3NknY9'
access_secret = 'xTQOdtxNgGg9ciYntAqrU6cJ8HbKnjuuxz08hGNOvHuNo'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#nltk.download()
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'the']
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
    r'[0-9]+th',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"""(?:[a-z][a-z'\-_]+[a-z])""",  # words with - and '
    r"""(?:[a-z][a-z"\-_]+[a-z])""",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    count_all.clear()
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



for status in tweepy.Cursor(api.user_timeline, id="@realdonaldtrump").items(10):
    # Process a single status
    i = i+1
    #tokens = word_tokenize(status.text)
    # for token in tokens:
    #terms_bigram = getBigrams(status.text)
   # print(count_all.most_common(5))
    #print(preprocess(status.text))
    print(status.text)
    print("******")