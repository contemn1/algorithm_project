#Create a bipartite graph of tweets and hashtags, create G^2 and then run SimRank on it to calcualte similarity scores
#map each tweet to a pos int ID and each hashtag to a neg int ID

import pdb, traceback, sys
import time
import csv
import operator
import simrank_tweets_2

def make_graph_csv(filename, graph_dict,hashtag_labels):
  csv = open(filename,"w")
  for v in graph_dict: 
      row=str(v)
      edges = graph_dict[v]
      for t in edges:
          row += ';' + str(t)
      csv.write(row + '\n')
  #for v in hashtag_labels.values():
    #csv.write(str(v) + '\n')
  csv.close()

#take in dictionary and return key : value list
def make_list(filename,input_dict):
  output = open(filename,'w')
  for head in input_dict: 
    row = str(head) + ' : ' + str(input_dict[head])
    output.write(row + '\n')
  output.close()

#take in list of tuples and return key : value list
def make_list_scores(filename, pair_list):
  output = open(filename,'w')
  for pair in pair_list: 
    row = str(pair[0]) + ' : ' + str(pair[1])
    output.write(row + '\n')
  output.close()

def main():
  start_time = time.time()
  #create the bipartite graph
  graph_dict = {}
  tweet_labels = {}
  hashtag_labels = {}
  i=1
  j = -1
  k=1
  f = open('C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_7_gen_2_plain.txt', 'r')
  hashtags = []
  hashtag_labels = {} #int : word
  hashtag_labels_flip = {} #word : int
  for tweet in f:
    if k > 1000: #b/c MemoryError, so only look at 500 tweets; k < 1000. Cannot use k > 5000. Even when using neg integers for hashtags
      break
    else:
      if '#' in tweet: #for now, only consider tweets with hashtags in them. Use negative integers instead of strings to save memory
        tweet_labels[i] = tweet
        graph_dict[i] = []
        splitted_tweet = tweet.split()
        for word in splitted_tweet:
          if '#' in word and len(word) > 1:
            if word not in graph_dict[i]:
              graph_dict[i].append(-j)
              #graph_dict[i].append(word)
            if word not in hashtag_labels_flip:  
              #hashtags.append(word)
              hashtag_labels[j] = word
              hashtag_labels_flip[word] = j
              #graph_dict[word] = [i]
              graph_dict[j] = [i]
              j -= 1
            else:
              #graph_dict[word].append(i)
              graph_dict[hashtag_labels_flip[word]].append(i)
        if graph_dict[i] == []:
          del graph_dict[i]
        else:
          i += 1
    k += 1

  graph_dict_sq = simrank_tweets_2.create_G_sq(graph_dict)  #create G^2 from bipartite graph
  scores = simrank_tweets_2.simrank(graph_dict, graph_dict_sq) #run simrank
  
  fn = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_7_gen_2_scores_2.txt'
  make_list_scores(fn,scores)

  filename = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_7_gen_2_bipgraph_2.txt'
  sorted_graph = sorted(graph_dict.items())
  make_list_scores(filename,sorted_graph)

  filename_2 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_7_gen_2_bipgraph_tweets_2.txt'
  make_list(filename_2,tweet_labels)

  filename_3 = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_7_gen_2_bipgraph_hashtags_2.txt'
  make_list(filename_3,hashtag_labels)

  #filename = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/data_7_gen_2_bipgraph.csv'
  #make_graph_csv(filename,graph_dict,hashtag_labels)

  print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)


