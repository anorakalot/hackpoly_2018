import json
from nltk.tokenize import TweetTokenizer
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams
import operator
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
    tweet = s
    tweet = tweet.lower()
    tokens = tknzr.tokenize(tweet)
    return tokens

#makes a list of all string punctuations plus some other things that have no meaning in tweets
punctuation = list(string.punctuation)
other_unimportants = ['rt','via','Via','RT','、','、' , '…','」','...','’','「','️','。','“']

print('\n' + "5 most common terms ")
#opens any json file and gives the 5 most common terms and the number of times they appear
with open('python_9.json','r') as f:
    #to make dictianry with number of times a token appears
    count_all = Counter()
    tknzr = TweetTokenizer()
    for line in f:
        #loads a line from the json file
        tweet = json.loads(line);
        #makes it so it only concerns itself witht the text part of the json line
        tweet = tweet['text']
        #list of things that should not count as important words telling us about public sentiment
        stop = list(stopwords.words('english')) + punctuation+ other_unimportants

        #terms_all = [term for term in pre_process(tweet)]

        #makes a list of all the tokens  - most stopwords and puncutation and other nonmeaning things

        terms_all_minus_stop = [term for term in pre_process(tweet) if term not in stop and not term.startswith(('#','&'))]

        #bigram for two words at the opposite ends of things in the stop list
        #terms_bigram = bigrams(stop)

        #terms_single = set(terms_all_minus_stop)

        #makes a dicionary with the token and the value being how many times its been said

        #count_all.update(terms_single)

        count_all.update(terms_all_minus_stop)

        #count_all.update(terms_all)

        #this line below takes tweet text and turns it into "tokens" of words
        #tokens = pre_process(tknzr.tokenize(tweet['text']))
    print(count_all.most_common(5))
    f.close()

print('\n' + "5 most common hashtags ")
#opens json file and gives the 5 most common hashtags
with open('python_9.json','r') as f:
    #to make dictianry with number of times a token appears
    count_all = Counter()
    tknzr = TweetTokenizer()
    for line in f:
        #loads a line from the json file
        tweet = json.loads(line);
        #makes it so it only concerns itself witht the text part of the json line
        tweet = tweet['text']
        #list of things that should not count as important words telling us about public sentiment
        stop = list(stopwords.words('english')) + punctuation+  other_unimportants
        #makes a list of all the tokens  - most stopwords and puncutation and other nonmeaning things
        terms_all_minus_stop = [term for term in pre_process(tweet) if term not in stop and term.startswith(('#'))]
        #makes a dicionary with the token and the value being how many times its been said
        count_all.update(terms_all_minus_stop)
        #this line below takes tweet text and turns it into "tokens" of words
        #tokens = pre_process(tknzr.tokenize(tweet['text']))
    print(count_all.most_common(5))
    f.close()


print('\n' + "5 most common term co-occurences ")
from collections import defaultdict
#term cocurrences

with open('python_9.json','r') as f:

#with open('python_3.json','r') as f:
    com = defaultdict(lambda: defaultdict(int))
    for line in f:
        stop = list(stopwords.words('english')) + punctuation+  other_unimportants
        tweet = json.loads(line)
        tweet = tweet['text']
        terms_only = [term for term in pre_process(tweet) if term not in stop and not term.startswith(('#','@'))]
        #builds matrix if in terms_only w1 and w2 are not equal
        for i in range(len(terms_only)-1):
            for j in range(i+1,len(terms_only)):
                w1,w2 = sorted([terms_only[i],terms_only[j]])
                if w1 != w2:
                    com[w1][w2] += 1

    com_max = []

    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))

    term_max = sorted(com_max,key = operator.itemgetter(1),reverse=True)
    print (term_max[:5])
