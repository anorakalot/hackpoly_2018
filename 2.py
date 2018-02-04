import json
from nltk.tokenize import TweetTokenizer
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams
import operator
import math

#tweet = "this is an example http://example.com"
#tweet = "RT @marcobonzanini: just an example! :D http://example.com" #NLP
#print(tknzr.tokenize(tweet))

file_to_open = str(input("Which file do you want to analyze..."))


#process to get tokens of words from tweets
def pre_process(s):
    tknzr = TweetTokenizer()
    tweet = s
    tweet = tweet.lower()
    tokens = tknzr.tokenize(tweet)
    return tokens

#makes a list of all string punctuations plus some other things that have no meaning in tweets
punctuation = list(string.punctuation)
other_unimportants = ['rt','via','Via','RT','、','、' , '…','」','...','’','「','️','。','“','”','🇷','🇺','__','『','ा','..']


print('\n' + "10 most common terms ")
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

        terms_all_minus_stop = [term for term in pre_process(tweet) if term not in stop and not term.startswith(('#','@','@','@')) and  term[0:5] != 'https'] #and 'https:' not in term)]

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
    print(count_all_minus_stop.most_common(10))
    f.close()


print('\n' + "10 most common hashtags ")
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
        terms_all_minus_stop = [term for term in pre_process(tweet) if term not in stop and term.startswith(('#'))]
        #makes a dicionary with the token and the value being how many times its been said
        count_all_hashtags.update(terms_all_minus_stop)
        #this line below takes tweet text and turns it into "tokens" of words
        #tokens = pre_process(tknzr.tokenize(tweet['text']))
    print(count_all_hashtags.most_common(10))
    f.close()

#opens and gives 5 most common term co occurences
print('\n' + "10 most common term co-occurences ")
from collections import defaultdict
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
    print (term_max[:10])


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

print ("\n")
print("Top Pos terms")
print (top_pos)


print ("\n")
print("Top Neg terms")
print (top_neg)
