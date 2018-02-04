import json
from nltk.tokenize import TweetTokenizer
from collections import Counter
from nltk.corpus import stopwords
import string

'''
with open('python.json','r') as f:
    line = f.readline()
    tweet = json.loads(line)
    print(json.dumps(tweet, indent = 4))
'''


#tweet = "this is an example http://example.com"
#tweet = "RT @marcobonzanini: just an example! :D http://example.com" #NLP
#print(tknzr.tokenize(tweet))

#process to get tokens of words from tweets
def pre_process(s):
    tknzr = TweetTokenizer()
    tokens = tknzr.tokenize(tweet)
    return tokens

#makes a list of all string punctuations plus some other things that have no meaning in tweets
punctuation = list(string.punctuation)

#opens any
with open('python_5.json','r') as f:
    count_all = Counter()
    tknzr = TweetTokenizer()
    for line in f:
        #loads a tweet from a
        tweet = json.loads(line);
        tweet = tweet['text']
        stop = list(stopwords.words('english')) + punctuation+ ['rt','via']
        #terms_all = [term for term in pre_process(tweet)]
        #makes a list of all the tokens  - most stopwords and puncutation and other nonmeaning things    
        terms_all_minus_stop = [term for term in pre_process(tweet) if term not in stop]
        #makes a dicionary with the token and the value being how many times its been said

        count_all.update(terms_all_minus_stop)
        #count_all.update(terms_all)

        #this line below takes tweet text and turns it into "tokens" of words
        #tokens = pre_process(tknzr.tokenize(tweet['text']))
    print(count_all.most_common(5))
