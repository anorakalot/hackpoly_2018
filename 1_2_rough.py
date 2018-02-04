import tweepy
from tweepy.auth import OAuthHandler
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
import time
from easygui import *
import json
from nltk.tokenize import TweetTokenizer
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams
import operator
import math
import os
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#keys and token for api acess
consumer_key = 'UPI6kKkPaNIHoj8a2AafnhIEA'
consumer_secret = 'Q0CeA7L3X5fFNzSeJe3KJ5sbASHI9BeigltrD8NBbcvYpZUoee'
access_token = '959874658257391616-dRDufRzaNZiisr2fzF9lV6mbAqxMplr'
access_secret = 'JCdzK3KAdSGcaLwrZ3owsYxitPLYwzQQ6z0drWK9WP0Dn'

#oauthhandler object api acess
auth = OAuthHandler(consumer_key,consumer_secret)
#use tokens to get access
auth.set_access_token(access_token,access_secret)

#use api variable for most operations with the twitter api
#sets up a api variable with authentication to use with our functions
api = tweepy.API(auth)

#print the whole json object given from cursor loops
def process_or_store(tweet):
    print(json.dumps(tweet))

'''
#loops through the home timeline api object
for status in tweepy.Cursor(api.home_timeline).items(10):
    process_or_store(status._json)
'''

#remakes Mylistener class in StreamListener class in tweepy
class MyListener(StreamListener):
    #opens data and writes it to a file

    def __init__(self,file_to_make_stream,time_limit):
        #self.num_tweets = 0;
        self.start_time = time.time()
        self.limit = time_limit;
        file_f = open(file_to_make_stream, 'w')
        file_f.truncate()
        file_f.close()

    def on_data(self,data):
        try:
            with open(file_to_make_stream,'a') as f:
                if ((time.time() - self.start_time) < self.limit):
                    f.write(data)
                    return True
                #ends if there was an error reading data
                else:
                    f.close()
                    return False
        except BaseException as e:
                print ("Error on_data: %s" % str(e))
                return True;
        #prints the error that happened when reading json data to the file
    def on_error(self,status):
        print(status)
        return True




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

def convert65536(s):
    #Converts a string with out-of-range characters in it into a string with codes in it.
    l=list(s);
    i=0;
    while i<len(l):
        o=ord(l[i]);
        if o>65535:
            l[i]="{"+str(o)+"ū}";
        i+=1;
    return "".join(l);


#makes a list of all string punctuations plus some other things that have no meaning in tweets

def print_data(file_to_open):
    #file_to_open = str(input("Which file do you want to analyze..."))


    punctuation = list(string.punctuation)
    other_unimportants = ['rt','via','Via','RT','、','、' , '…','」','...','’','「','️','。','“','”','🇷','🇺','__','『','ा','..','	🔥']


    title ="10 most common terms "
    #opens any json file and gives the 5 most common terms and the number of times they appear
    with open(file_to_open,'r') as f:
        #to make dictianry with number of times a token appears
        count_all_minus_stop = Counter()
        count_all_terms = Counter()
        for line in f:
            #loads a line from the json file
            tweet = json.loads(line);
            #makes it so it only concerns itself witht the text part of the json line
            if 'text' in tweet:
                tweet = tweet["text"]
            else:
                tweet = ""
            #list of things that should not count as important words telling us about public sentiment
            stop = list(stopwords.words('english')) + punctuation+ other_unimportants

            terms_all = [term for term in pre_process(tweet)]

            #makes a list of all the tokens  - most stopwords and puncutation and other nonmeaning things

            terms_all_minus_stop = [convert65536(term) for term in pre_process(tweet) if term not in stop and not term.startswith(('#','@','@','@')) and  term[0:5] != 'https' ] #and 'https:' not in term)]

            #bigram for two words at the opposite ends of things in the stop list
            #terms_bigram = bigrams(stop)


            #dont know what this does
            #terms_single = set(terms_all_minus_stop)

            #makes a dicionary with the token and the value being how many times its been said

            #count_all.update(terms_single)
            count_all_terms.update(terms_all)
            count_all_minus_stop.update(terms_all_minus_stop)

            #count_all.update(terms_all)

            #this line below takes tweet text and turns it into "tokens" of words
            #tokens = pre_process(tknzr.tokenize(tweet['text']))
        str_1 = str(count_all_minus_stop.most_common(10))
        msgbox(str_1,title)
        #str_2 = str_2.strip['[]']
        f.close()

        plt.bar(range(len(count_all_minus_stop.most_common(10))),list(dict(count_all_minus_stop.most_common(10)).values()),align = 'center')
        plt.xticks(range(len(count_all_minus_stop.most_common(10))),list(dict(count_all_minus_stop.most_common(10)).keys()))
        plt.ylabel("Occurences")
        plt.show()
        '''
        df = pd.DataFrame.from_dict(count_all_minus_stop.most_common(10))
        #print(df.head())
        df[0].value_counts().plot(kind='hist')
        plt.axis([40, 160, 0, 100])
        plt.show()
        '''


    title_2 = "10 most common hashtags "
    #opens json file and gives the 5 most common hashtags
    with open(file_to_open,'r') as f:
        #to make dictianry with number of times a token appears
        count_all_hashtags = Counter()
        for line in f:
            #loads a line from the json file
            tweet = json.loads(line);
            #makes it so it only concerns itself with the text part of the json line
            if 'text' in tweet:
                tweet = tweet["text"]
            else:
                tweet = ""
            #list of things that should not count as important words telling us about public sentiment
            stop = list(stopwords.words('english')) + punctuation+  other_unimportants
            #makes a list of all the tokens  - most stopwords and puncutation and other nonmeaning things
            terms_all_minus_stop = [convert65536(term) for term in pre_process(tweet) if term not in stop and term.startswith(('#')) ]
            #makes a dicionary with the token and the value being how many times its been said
            count_all_hashtags.update(terms_all_minus_stop)
            #this line below takes tweet text and turns it into "tokens" of words
            #tokens = pre_process(tknzr.tokenize(tweet['text']))
        str_2 = str(count_all_hashtags.most_common(10))
        msgbox(str_2,title_2)
        f.close()
        plt.bar(range(len(count_all_hashtags.most_common(10))),list(dict(count_all_hashtags.most_common(10)).values()),align = 'center')
        plt.xticks(range(len(count_all_hashtags.most_common(10))),list(dict(count_all_hashtags.most_common(10)).keys()))
        plt.ylabel("Occurences")
        plt.show()

    #opens and gives 5 most common term co occurences
    title_3 = ("10 most common term co-occurences ")

    #term cocurrences

    with open(file_to_open,'r') as f:

    #with open('python_3.json','r') as f:
        com = defaultdict(lambda: defaultdict(int))
        for line in f:
            stop = list(stopwords.words('english')) + punctuation+  other_unimportants
            tweet = json.loads(line)
            if 'text' in tweet:
                tweet = tweet["text"]
            else:
                tweet = ""
            terms_only = [term for term in pre_process(tweet) if term not in stop and not term.startswith(('#','&','@')) and  term[0:5] != 'https']
            #terms_only = [term for term in pre_process(tweet) if term not in stop and not term.startswith(('&','@')) and  term[0:5] != 'https']
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

        str_3 = str(term_max[:10])

        str_3 = convert65536(str_3)
        title_3 = convert65536(title_3)
        msgbox(str_3,title_3)


        tuple_term = list(zip(*term_max[:10]))[0]

        count_occurences = list(zip(*term_max[:10]))[1]

        x_position = np.arange(len(list(zip(*term_max[:10]))[0]))
        plt.bar(range(len(tuple_term)), count_occurences,align = 'center')
        plt.xticks(x_position,tuple_term)
        plt.ylabel("Occurences")
        plt.show()

        '''
        plt.bar(range(len(term_max[:10])),list(term_max[:10].values()),align = 'center')
        plt.xticks(range(len(term_max[:10])),list(dict(count_all_minus_stop.most_common(10)).keys()))
        plt.show()
        '''
    #Starting Semantic analysis
    positive_vocab = []
    negative_vocab = []
    # n_docs is the total n. of tweets
    p_t = {}
    p_t_com = defaultdict(lambda : defaultdict(int))
    n_docs = sum(1 for line in open(file_to_open))
    for term, n in count_all_terms.items():
        #p(t) = DF(t)/|D|
        p_t[term] = n / n_docs
        #p(t1^t2a) = DF(t1^t2)/|D|
        for t2 in com[term]:
            p_t_com[term][t2] = com[term][t2] / n_docs


    #getting the pos and neg words from file

    with open("positive-words.txt") as f:
        for line in f:
            line = line.rstrip('\n')
            positive_vocab.append(line)
    with open("negative-words.txt") as f:
        for line in f:
            line = line.rstrip('\n')
            negative_vocab.append(line)



    '''
    file_neg = open("negative-words.txt")
    file_neg_list = file_neg.readlines()
    file_neg.close()
    '''
    '''
    for f in positive_vocab:#negative_vocab:
        #f = f.strip("\n")
        print (f)
    '''

    #calculates the  chosen measure of “closeness”  Pointwise Mutual Information (PMI)
    pmi = defaultdict(lambda : defaultdict(int))
    #PMI(t1,t2) = log(P())t1 ^ t2)/p(t1)*p(t2))
    for t1 in p_t:
        for t2 in com[t1]:
            denom = p_t[t1] * p_t[t2]
            pmi[t1][t2] = math.log2(p_t_com[t1][t2]/denom)

    #makes the semantic_orientation dictianry difference between closeness of positive_vocab and negative_vocab
    semantic_orientation = {}
    for term , n in p_t.items():
        positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
        negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
        semantic_orientation[term] = positive_assoc - negative_assoc

    #sort the semantic_orientation dictionary
    semantic_sorted = sorted(semantic_orientation.items(),key = operator.itemgetter(1),reverse = True)
    top_pos = semantic_sorted[:10]
    top_neg = semantic_sorted[-10:]


    title_4 = "Top Sentimental Positive terms in tweets"
    str_4 = str(top_pos)
    msgbox(str_4,title_4)
    pos_term = list(zip(*top_pos))[0]
    pos_rating = list(zip(*top_pos))[1]
    x_position = np.arange(len(pos_term))
    plt.bar(x_position,pos_rating,align = 'center')
    plt.xticks(x_position,pos_term)
    plt.ylabel("Positive Semantic Orientation Score")
    plt.show()

    title_5 = "Top Semantical Negative terms in tweets"
    str_5 = str(top_neg)
    msgbox(str_5,title_5)

    neg_term = list(zip(*top_neg))[0]
    neg_rating = list(zip(*top_neg))[1]
    x_position = np.arange(len(neg_term))
    plt.bar(x_position,neg_rating,align = 'center')
    plt.xticks(x_position,neg_term)
    plt.ylabel("Negative Semantic Orientation Score")
    plt.show()


    with open(file_to_open,'r') as f:
        geo_data = {
        "type": "FeatureCollection",
        "features":[]
        }
        for line in f:
            tweet = json.loads(line)
            if tweet['coordinates']:
                geo_json_feature = {
                "type": "Feature",
                "geometry":tweet['coordinates'],
                "properties":{
                "text":tweet['text'],
                "created_at": tweet['created_at']
                }
                }
                geo_data['features'].append(geo_json_feature)
    with open('geo_data.json','w') as fout:
        fout.write(json.dumps(geo_data, indent = 4))
        print("geo data json being written")


choice = "dummy_value"
while(choice != "exit"):
    msg = "What do you want to do"
    title = "Twitter Sentiment Analysis"
    choices = ["make_new_tweet_stream","list_directory","sentiment_analyzation", "look_at_json_files" , "exit"]
    choice = choicebox(msg,title,choices)

    if (choice ==  "make_new_tweet_stream"):
        #filter_str = str(input("which filter?..."))
        filter_str = str(enterbox("Which filter for your new_stream "))
        file_to_make_stream = str(enterbox("name of new file? (Beware adding in the same string for a previously existing file will erase that file!)"))
        #makes a new stream object
        time_limit = int(enterbox("Please enter seconds to make for your new tweet stream "))
        msg = "Do you want to continue?"
        title = "Please Confirm"
        if ccbox(msg, title):     # show a Continue/Cancel dialog
            twitter_stream = Stream(auth,MyListener(file_to_make_stream,time_limit))
            #makes the .json file filled with twitter json data
            twitter_stream.filter(languages=["en"],track=[filter_str])

            pass  # user chose Continue
        else:  # user chose Cancel
            choice = "dummy_value"

    elif  (choice == "list_directory"):
        os_string = os.listdir()
        msgbox(os_string)
    elif (choice == "sentiment_analyzation"):
        checker = True
        while checker:
            file_to_open = str(enterbox("Which file do you want to analyze "))
            if (os.path.isfile(file_to_open)!= True):
                msgbox("not a valid file name")
            else:
                print_data(file_to_open)
                checker = False

    elif (choice == "look_at_json_files"):
        checker = True
        while checker:
            file_to_look_at = str(enterbox("Which json file do you want to look at "))
            if enterbox():
                if(os.path.isfile(file_to_look_at) != True):
                    msgbox("not a valid json file name")
                else:
                    filename = os.path.normcase(file_to_look_at)
                    f = open(filename, "r")
                    text = f.readlines()
                    f.close()
                    codebox(text)
                    checker = False
            else:
                checker=False
