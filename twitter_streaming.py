#Listener code: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
#Import the necessary methods from tweepy library
import pdb
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import operator
import os
import pickle

#Variables that contains the user credentials to access Twitter API 
consumer_key = 'S8XtmVeNeYp0F5s3Ba8294rOD'
consumer_secret = '7qbCN3piFWNMixcKCNgf8jNpv1TR71zWyahm5xq7CGE2o4LI0p'
access_token = '848576341700206592-THBDf8XxuL84ok0bwH7YKovFBFKezTS'
access_token_secret = 'qebXmt5NFERtGEnulgxD7MxIf7HvrXO3Tja2V8l1uVvNE'


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

#use hashtags from the last iteration to search for related hashtags in the Listener
def get_hashtags():
  cwd = os.getcwd()
  X=8 #dataset ID
  Y=0 #prev gen you get your hashtags from
  hashtag_freqs = {} #store by hashtag : freq
  f = open(cwd + '\\data_'+str(X)+'_gen_'+str(Y)+'.txt', 'r')
  for tweet in f:
    if '#' in tweet:  #only consider tweets with hashtags
      splitted_tweet = tweet.split()
      for word in splitted_tweet:
        if word[0] == '#' and len(word) > 1: #do not consider words that are just the symbol '#'
          if word in hashtag_freqs:
            hashtag_freqs[word] += 1  #track frequency to take only the top 10 most popular hashtags
          else:
            hashtag_freqs[word] = 1

  #hashtag_freqs.pop('#', None)  #remove '#'
  sorted_freqs = sorted(hashtag_freqs.items(), key=operator.itemgetter(1))  #sort 
  sorted_freqs.reverse()
  most_pop = [pair[0] for pair in sorted_freqs][0:int(round(len(sorted_freqs)/4))] #top 25%

  #get prev hashtags from pickle
  #prev_hashtags = pickle.load(open(cwd + '\\data_'+str(X)+'_hashtag_gen_'+str(Y)+'.p', 'rb'))
  prev_hashtags = ['#music','#concert','#politics','#trump','#russia','#brexit','#gaming','#gamers','#pc','#xbox']

  """
  new_top_10 = [] #take the top 10 most popular NEW hashtags in this iteration step
  i=0
  while len(new_top_10) < 11:
    if sorted_freqs[i] not in prev_hashtags:  #only add in new hashtags 
      new_top_10.append(sorted_freqs[i])
      i += 1
  """

  new_filter = list(set(prev_hashtags + most_pop)) #old hashtags plus top 10 new hashtags
  fn = cwd + '\\data_'+str(X)+'_hashtag_gen_'+str(Y+1)+'.txt'
  with open(fn,'w') as fn:
    for hashtag in new_filter:
      fn.write(str(hashtag) + '\n') #store as first line for use in gen Y+2. 
  pickle.dump(new_filter, open(cwd + '\\data_'+str(X)+'_hashtag_gen_'+str(Y+1)+'.p', 'wb'))
  #store new hashtags as both txt and pickle files so they can be reused in next gen

  return new_filter

if __name__ == '__main__':
    #keywords = get_hashtags()
    #pdb.set_trace()

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords
    
    #gen 1 and after
    keywords = get_hashtags()
    stream.filter(track=keywords)

    #initial
    #stream.filter(track=['#music','#concert','#politics','#trump','#russia','#brexit','#gaming','#gamers','#pc','#xbox'])