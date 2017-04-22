import pdb, traceback, sys
import operator
import numpy
from simrank_fns import *
import os
import pickle

#given an input tweet, find similar tweets and hashtags

def get_tweets(graph_dict, input_hashtag_tweets, tweet_ids, input_hashtag, similar_hashtags, cat):
  similar_tweets = []
  for (hashtag, score) in similar_hashtags:
    tweets = graph_dict[hashtag] #for hashtags of that tweet
    for t in tweets:
      if t not in input_hashtag_tweets and t not in similar_tweets: #find relative complement (no tweets contain that hashtag) and prevent duplicates
        similar_tweets.append(t)
  similar_hashtags = list(set(similar_hashtags))

  cwd = os.getcwd()
  fn = cwd + '\\data_7_gen_2_hashtag_'+str(input_hashtag)+'_simtweets_'+cat+'.txt'
  output = open(fn,'w') 
  if similar_tweets == []:
    output.write('No new tweets found')
  else:
    for t in similar_tweets:
      output.write(str(tweet_ids[t]) + '\n')
  output.close()


def get_hashtags(graph_dict, input_hashtag, hashtag_ids, similar_hashtags, cat):
  cwd = os.getcwd()
  fn = cwd + '\\data_7_gen_2_hashtag_'+str(input_hashtag)+'_simhashtags_'+cat+'.txt'
  output = open(fn,'w') 
  if similar_hashtags == []:
    output.write('No new hashtags found')
  else:
    for ID in similar_hashtags: #can't use id b/c built-in fn; var are case sensitive
      hashtag = hashtag_ids[ID[0]]
      output.write(hashtag + '\n')
  output.close()

def main():
  #load G, scores and id labels
  cwd = os.getcwd()
  data_file = 'data_1'
  header = cwd + '\\' + data_file
  graph_dict = pickle.load( open(header +'_bigraph.p', "rb" ) )
  tweet_ids = pickle.load( open(header +'_tweets.p', "rb" ) ) 
  hashtag_ids = pickle.load( open(header +'_hashtags.p', "rb" ) ) 
  scores = pickle.load( open(header +'_scores.p', "rb" ) ) 

  #from user input, get input_hashtag
  rev_hashtag_ids = {v: k for k, v in hashtag_ids.iteritems()} #reverse hashtag_ids to get hashtag : id
  input_hashtag = int(rev_hashtag_ids[sys.argv[1]])

  #convert set of hashtags into the tweet that matches it. check graph_dict.values() to see if any sets match the set of hashtags
  #multiple sets may contain multiple hashtags. For simplicity, just choose one. 
  if input_hashtag not in graph_dict:
    return 'Hashtag not found in currently stored data'
  input_hashtag_tweets =  graph_dict[input_hashtag] #get hashtag neighbors of input tweet
  
  related_hashtags = {}
  stop_signal = 'on'
  for (x,y) in scores: 
    if x != y:
      if x == input_hashtag:  #only eval x b/c pairs are symmetrical
        stop_signal = 'off'
        related_hashtags[y] = scores[(x,y)] #get all tweets w/ a score > 0 relative to input_tweet

  if stop_signal == 'on':
    return 'No similar hashtags found'

  sorted_rel_scores = sorted(related_hashtags.items(), key=operator.itemgetter(1))
  sorted_rel_scores.reverse()

  #sort hashtags into categories of scores. The % are arbitrary, for now.
  #get histogram of scores. High: top 10%. Mid: 10-20%. Low: 20-30%
  high = sorted_rel_scores[0 : int(len(sorted_rel_scores) * .1)]
  mid = sorted_rel_scores[int(len(sorted_rel_scores) * .1) : int(len(sorted_rel_scores) * .2)]
  low = sorted_rel_scores[int(len(sorted_rel_scores) * .2) : int(len(sorted_rel_scores) * .3)]
  
  get_tweets(graph_dict, input_hashtag_tweets, tweet_ids, input_hashtag, high, 'high')
  get_tweets(graph_dict, input_hashtag_tweets, tweet_ids, input_hashtag, mid, 'mid')
  get_tweets(graph_dict, input_hashtag_tweets, tweet_ids, input_hashtag, low, 'low')

  get_hashtags(graph_dict, input_hashtag, hashtag_ids, high, 'high')
  get_hashtags(graph_dict, input_hashtag, hashtag_ids, mid, 'mid')
  get_hashtags(graph_dict, input_hashtag, hashtag_ids, low, 'low')

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
