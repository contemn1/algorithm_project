import pdb, traceback, sys
import operator
import numpy
from simrank_fns import *
import os
import pickle

#given an input tweet, find similar tweets and hashtags

def get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, similar_tweets, cat, header):
  similar_hashtags = []
  for (tweet, score) in similar_tweets:
    hashtags = graph_dict[tweet] #for hashtags of that tweet
    for h in hashtags:
      if h not in input_tweet_hashtags and h not in similar_hashtags: #find relative complement and prevent duplicates
        similar_hashtags.append(h)
  similar_hashtags = list(set(similar_hashtags))

  cwd = os.getcwd()
  fn = header + '_tweet_'+ str(input_tweet) +'_simhashtags_'+cat+'.txt'
  output = open(fn,'w') 
  if similar_hashtags == []:
    output.write('No new hashtags found')
  else:
    for h in similar_hashtags:
      output.write(str(hashtag_ids[h]) + '\n')
  output.close()


def get_tweets(graph_dict, input_tweet, tweet_ids, similar_tweets, cat, header):
  cwd = os.getcwd()
  fn = header + '_tweet_'+ str(input_tweet) +'_simtweets_'+cat+'.txt'
  output = open(fn,'w') 
  if similar_tweets == []:
    output.write('No new tweets found')
  else:
    for ID in similar_tweets: #can't use id b/c built-in fn; var are case sensitive
      tweet = tweet_ids[ID[0]]
      output.write(tweet + '\n')
  output.close()

def main():
  #load G, scores and id labels
  cwd = os.getcwd()
  X = 8
  Y = 1
  data_file = 'data_' + str(X) + '_gen_'+ str(Y)
  header = cwd + '\\' + data_file
  graph_dict = pickle.load( open(header +'_bigraph.p', "rb" ) )
  tweet_ids = pickle.load( open(header +'_tweets.p', "rb" ) ) 
  hashtag_ids = pickle.load( open(header +'_hashtags.p', "rb" ) ) 
  scores = pickle.load( open(header +'_scores.p', "rb" ) ) 

  #from user input, get input_tweet (during create_graph, you assigned an id to input_tweet, so use that)
  #rev_tweet_ids = ... #reverse tweet_ids
  #input_tweet = rev_tweet_ids[user_input]

  #convert set of hashtags into the tweet that matches it. check graph_dict.values() to see if any sets match the set of hashtags
  #multiple sets may contain multiple hashtags. For simplicity, just choose one. 
  if sys.argv[1].isdigit() == False:
    return 'Enter a positive integer for system argument'
  elif int(sys.argv[1]) not in graph_dict:
    return 'Enter a valid tweet id'
  input_tweet = int(sys.argv[1])
  input_tweet_hashtags =  graph_dict[input_tweet] #get hashtag neighbors of input tweet
  
  related_tweets = {}
  stop_signal = 'on'
  for (x,y) in scores: 
    if x != y:
      if x == input_tweet:  #only eval x b/c pairs are symmetrical
        stop_signal = 'off'
        related_tweets[y] = scores[(x,y)] #get all tweets w/ a score > 0 relative to input_tweet

  if stop_signal == 'on':
    return 'No similar tweets found'

  sorted_rel_scores = sorted(related_tweets.items(), key=operator.itemgetter(1))
  sorted_rel_scores.reverse()

  #sort hashtags into categories of scores. The % are arbitrary, for now. Don't output too many options for the user to read
  #High: top 20%. Mid: 20-30%. Low: 30-40%
  high = sorted_rel_scores[0 : int(len(sorted_rel_scores) * .2)]
  mid = sorted_rel_scores[int(len(sorted_rel_scores) * .2) : int(len(sorted_rel_scores) * .3)]
  low = sorted_rel_scores[int(len(sorted_rel_scores) * .3) : int(len(sorted_rel_scores) * .4)]

  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, high, 'high', header)
  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, mid, 'mid', header)
  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, low, 'low', header)

  get_tweets(graph_dict, input_tweet, tweet_ids, high, 'high', header)
  get_tweets(graph_dict, input_tweet, tweet_ids, mid, 'mid', header)
  get_tweets(graph_dict, input_tweet, tweet_ids, low, 'low', header)

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
