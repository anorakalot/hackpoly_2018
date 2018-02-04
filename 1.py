import tweepy
from tweepy.auth import OAuthHandler
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
import time

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

    def __init__(self):
        #self.num_tweets = 0;
        self.start_time = time.time()
        self.limit = 1800;
        file_f = open('python_tem.json', 'w')
        file_f.truncate()
        file_f.close()

    def on_data(self,data):
        try:
            with open('mcdonalds.json','a') as f:
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

filter_str = str(input("which filter?..."))
#makes a new stream object

twitter_stream = Stream(auth,MyListener())
#makes the .json file filled with twitter json data
twitter_stream.filter(languages=["en"],track=[filter_str])
