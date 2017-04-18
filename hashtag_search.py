import pdb, traceback, sys
import time
import operator
from simrank_fns import *

def main():
  start_time = time.time()
  #get node_scores, G^2, and the dicts that pair tweets w/ id and hashtags w/ id
  data_file = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 3/data_7_gen_2_plain.txt'
  graph_dict, tweet_ids, hashtag_ids = create_graph(data_file)
  filename = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 3/data_7_gen_2_bigraph.txt'
  sorted_graph = sorted(graph_dict.items())
  make_list_scores(filename,sorted_graph)

  filename_2 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 3/data_7_gen_2_tweets.txt'
  make_list(filename_2,tweet_ids)

  filename_3 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 3/data_7_gen_2_hashtags.txt'
  sorted_hashtag_ids = collections.OrderedDict(sorted(hashtag_ids.items()))
  make_list(filename_3, sorted_hashtag_ids)

  graph_dict_sq = create_G_sq(graph_dict)  #create G^2 from bipartite graph
  scores, sorted_scores = simrank(graph_dict, graph_dict_sq) #run simrank

  fn = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 3/data_7_gen_2_scores.txt'
  make_list_scores(fn, sorted_scores)

  print("--- %s seconds ---" % (time.time() - start_time))

  #from user input, get input_tweet (during create_graph, you assigned an id to input_tweet, so use that)
  #as you're running make_g_sq, find related tweets to speed things up
  #extract hashtags from input tweet
  input_tweet = 7
  input_tweet_hashtags = ['#hits', '#musique' '#pop', '#np']
  #input_tweet_hashtags =  in graph_dict[input_tweet]: #get hashtag neighbors of input tweet

  related_tweets = {}

  stop_signal = 'on'
  for (x,y) in graph_dict_sq: 
    if x != y:
      if x == input_tweet:  #only eval x b/c pairs are symmetrical
        stop_signal = 'off'
        related_tweets[y] = scores[(x,y)] #get all tweets w/ a score > 0 relative to input_tweet

  if stop_signal == 'on':
    return 'No results found'

  sorted_rel_scores = sorted(related_tweets.items(), key=operator.itemgetter(1))
  sorted_rel_scores.reverse()
  similar_tweets = sorted_rel_scores[0:10] #get the 100 most similar tweets

  similar_hashtags = []
  for (tweet, score) in similar_tweets:
    hashtags = graph_dict[tweet] #for hashtags of that tweet
    for h in hashtags:
      hashtag = hashtag_ids[h]
      if hashtag not in input_tweet_hashtags and hashtag not in similar_hashtags: #find relative complement and prevent duplicates
        similar_hashtags.append(h)

  similar_hashtags = list(set(similar_hashtags))
  fn_2 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 3/data_7_gen_2_tweet_7_simhash.txt'
  output = open(fn_2,'w') 
  for h in similar_hashtags:
    output.write(str(hashtag_ids[h]) + '\n')
  output.close()

  #sort hashtags into categories of scores
  

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
