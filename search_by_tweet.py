import pdb, traceback, sys
import operator
import numpy
from simrank_fns import *
import os
import pickle

#given an input tweet, find similar tweets and hashtags

def get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, similar_tweets, cat):
  similar_hashtags = []
  for (tweet, score) in similar_tweets:
    hashtags = graph_dict[tweet] #for hashtags of that tweet
    for h in hashtags:
      if h not in input_tweet_hashtags and h not in similar_hashtags: #find relative complement and prevent duplicates
        similar_hashtags.append(h)
  similar_hashtags = list(set(similar_hashtags))

  cwd = os.getcwd()
  fn = cwd + '\\data_7_gen_2_tweet_'+str(input_tweet)+'_simhashtags_'+cat+'.txt'
  output = open(fn,'w') 
  if similar_hashtags == []:
    output.write('No new hashtags found')
  else:
    for h in similar_hashtags:
      output.write(str(hashtag_ids[h]) + '\n')
  output.close()


def get_tweets(graph_dict, input_tweet, tweet_ids, similar_tweets, cat):
  cwd = os.getcwd()
  fn = cwd + '\\data_7_gen_2_tweet_'+str(input_tweet)+'_simtweets_'+cat+'.txt'
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
  graph_dict = pickle.load( open(cwd + '\\data_7_gen_2_bigraph.p', "rb" ) )
  tweet_ids = pickle.load( open(cwd + '\\data_7_gen_2_tweets.p', "rb" ) ) 
  hashtag_ids = pickle.load( open(cwd + '\\data_7_gen_2_hashtags.p', "rb" ) ) 
  scores = pickle.load( open(cwd + '\\data_7_gen_2_scores.p', "rb" ) ) 

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

  #sort hashtags into categories of scores. The % are arbitrary, for now.
  #get histogram of scores. High: top 10%. Mid: 10-20%. Low: 20-30%
  high = sorted_rel_scores[0 : int(len(sorted_rel_scores) * .1)]
  mid = sorted_rel_scores[int(len(sorted_rel_scores) * .1) : int(len(sorted_rel_scores) * .2)]
  low = sorted_rel_scores[int(len(sorted_rel_scores) * .2) : int(len(sorted_rel_scores) * .3)]
  
  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, high, 'high')
  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, mid, 'mid')
  get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, low, 'low')

  get_tweets(graph_dict, input_tweet, tweet_ids, high, 'high')
  get_tweets(graph_dict, input_tweet, tweet_ids, mid, 'mid')
  get_tweets(graph_dict, input_tweet, tweet_ids, low, 'low')

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
